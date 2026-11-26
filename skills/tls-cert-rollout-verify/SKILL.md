---
name: tls-cert-rollout-verify
description: Verify from outside that a renewed TLS certificate is served on every address of a host before the old one expires, with distinct verdicts for rolling, old, unexpected and probe-failed.
---

# TLS certificate rollout verify

"The certificate was renewed" and "every edge serves the new certificate" are different facts. One successful request proves only the address it happened to reach. A monitor that returns zero samples proves nothing at all, yet is often reported as an outage.

## Inputs

- The hostnames in scope, exactly as approved.
- The new certificate's serial, expiry and issuer, plus the old serial and expiry. If the host serves more than one certificate type (for example RSA and ECDSA), list every expected serial.
- The deadline after which the old certificate must no longer appear.
- At least two vantage points on different networks.

## 1. Probe every address with SNI

```bash
H=<hostname>
# Cap each connection at 10 seconds (on macOS, gtimeout comes with coreutils)
limit() {
  if command -v timeout >/dev/null; then timeout 10 "$@"
  elif command -v gtimeout >/dev/null; then gtimeout 10 "$@"
  else "$@"; fi
}
command -v timeout >/dev/null || command -v gtimeout >/dev/null || echo "no timeout tool: a dead address can hang the run" >&2
{ dig +short A "$H" | grep -E '^[0-9]+(\.[0-9]+){3}$'; dig +short AAAA "$H" | grep ':'; } |
while read -r ip; do
  case "$ip" in *:*) target="[$ip]:443" ;; *) target="$ip:443" ;; esac
  raw=$(limit openssl s_client -connect "$target" -servername "$H" -verify_hostname "$H" </dev/null 2>/dev/null)
  echo "== $ip"
  printf '%s\n' "$raw" | grep -m1 'Verify return code'
  printf '%s\n' "$raw" | openssl x509 -noout -serial -enddate -issuer 2>/dev/null || echo "NO-SAMPLE"
  printf '%s\n' "$raw" | openssl x509 -noout -text 2>/dev/null | grep -A1 'Subject Alternative Name'
done
```

Notes:
- No `==` lines at all means no address was resolved. That is `probe_failed`.
- Some bundled OpenSSL-compatible builds lack `-verify_hostname`, which makes every sample fail. Use a current OpenSSL.
- Each handshake returns one certificate. Where a host serves several types, repeat the probe while restricting signature algorithms (for example `-sigalgs ECDSA+SHA256`, then `-sigalgs RSA-PSS+SHA256:RSA+SHA256`), and confirm from the output that you received the type you asked for. A type you never sampled is unverified.
- Probe each address at least twice, and also make one direct connection by hostname.
- Some VPNs, DNS proxies and sandboxes return placeholder addresses that hide the real edges. If the addresses look private or synthetic, probe from another network.
- An anycast address can reach different locations from different places, which is why one vantage point is not enough.

## 2. Check each sample

Serial matches an expected new serial (normalise case and separators), expiry matches, the subject alternative names cover the hostname, the chain verifies, and the old serial appears nowhere.

## 3. Verdict

| Verdict | Meaning | Wake a person? |
|---|---|---|
| `ok` | every sample shows a new serial and verifies, and every expected certificate type was sampled | no |
| `rolling` | new and old both seen | only after the deadline |
| `old_only` | only the old serial seen | only after the deadline |
| `unexpected` | a serial that is neither, a wrong name, or a failed chain | yes, now |
| `probe_failed` | no usable samples, or the tool broke | fix the probe first |

Suggested exit codes for a script: `0` nothing needs a person yet, `1` wake, `2` probe failed.

**Zero samples never equals certificate failure.** Report reachability separately from certificate state. Before telling anyone about `probe_failed` or a surprising result, take one direct reading by a different method.

If some address is unreachable while others pass, say which. The result then covers only the sampled addresses.

## 4. Follow-through

- If an old serial remains, retry after about ten minutes to allow for propagation. Set the final deadline comfortably before the old certificate expires.
- On a pass, write one line (serials, expiry, addresses, vantage points, time) and stay quiet.
- On an alert, send one evidence table with addresses and serials to whoever owns the deployment.
- Retire a one-off check after it passes.

## Never

- Never renew, reissue or deploy as part of verification.
- Never probe hosts outside the approved list.
- Never print or copy private keys or certificate account keys.

## When to use

- During a certificate renewal or replacement window.
- Before an old certificate expires.
- When a certificate monitor reports a probe failure or conflicting results.

## How to use

1. Copy the `tls-cert-rollout-verify` folder into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project.
2. Ask Claude Code to use the skill by name.
3. Example prompts:
   - "Use the tls-cert-rollout-verify skill on <hostname>. The new serial is <serial>, the old is <serial>, and the deadline is <time>."
   - "My monitor says the certificate check failed with zero samples. Use tls-cert-rollout-verify to separate a broken probe from a bad certificate."
