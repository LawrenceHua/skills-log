---
name: past-behavior-interviews
description: Plan and judge customer or user interviews so they collect evidence about past behavior instead of compliments, generic claims, and feature ideas.
---

# Past-behavior interviews

People tell you what they think you want to hear. They are not lying maliciously; they are being polite, helpful, or avoiding conflict. The result is not a wrong answer but a confident answer that was never evidence, and it can survive into a roadmap because nobody can point to the moment it became "true". This skill keeps interviews, and summaries of interviews, anchored to what people actually did. The core rules follow the widely taught customer-discovery approach popularized by Rob Fitzpatrick's book *The Mom Test*; this is a compact restatement in working form.

## Three rules for asking

1. **Talk about their life, not your idea.** If you can swap your product for a competitor's, or for nothing, and the question still works, it was about your idea. Replace "Would a reminder tool help you?" with "Walk me through the last time this came up. What happened?"
2. **Ask about specific past events, not generics or futures.** Past behavior is data; future intention is a story about a person they have not met. Replace "Would you pay for this?" or "How often do you usually...?" with "When did you last do it? What did you do that day? What did it cost you?"
3. **Talk less and listen more.** The moment someone describes a problem and you say "that's exactly what we built", the interview becomes a pitch and the data stops.

## Three kinds of bad data

Anything that is not about past behavior is one of these. Each produces a false positive: you feel more confident and are less right.

| Type | Sounds like | Why it is worthless |
|---|---|---|
| Compliment | "Great idea", "I love it" | Politeness; costs them nothing. |
| Fluff | "I usually...", "I would probably...", "I'd definitely buy that" | Generics and futures about an imagined self. |
| Idea | "You should add X", "What if it also did Y" | A design opinion, not a need. |

A compliment is the most dangerous because it feels like validation and arrives exactly when you are hoping for it. Deflect it, then ask about the last time the problem occurred.

## Working method

### Before the call

1. Write the one thing you most need to learn (is the problem real, how is it handled today, what does it cost).
2. Draft 5-8 questions about past events: last occurrence, what they tried, what they paid, who else was involved, what they use now.
3. Cross out any question that mentions your solution or asks for a prediction.

### During the call

1. Open with their context and role, not your pitch.
2. Follow the energy: when they mention a workaround, a tool they pay for, or a recent frustration, ask "tell me more about that" and "what happened next".
3. Ask why it matters, and what they have already tried to fix it. A workaround someone already built is stronger evidence than any answer to "would you use this?".
4. Capture exact words, not paraphrase.
5. Close by asking for a commitment that costs something (a follow-up time, an introduction, a pilot, a deposit), not for an opinion.

### After the call

1. Record verbatim quotes next to your interpretation, kept separate.
2. Count how many people described the same problem unprompted. Two is a coincidence; five is a pattern.
3. Note what you expected to hear and did not. Those absences are findings you will be tempted to explain away.
4. Classify every statement as behavior (did), commitment (will pay or give something), or opinion (said/might). Only the first two are evidence.

## Judging someone else's interview summary

Apply one test to every claim: does it describe something someone did, or something someone said they might do? If the second, it is a hypothesis, and the summary should label it as one. Flag summaries that contain no quotes, no past events, or no commitments.

## When to use

- Before writing questions for a discovery call or user research session.
- When reviewing interview notes or a summary written by a person or an agent.
- When a roadmap item is justified only by "customers said they'd love it".

## How to use

1. Copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project.
2. Ask Claude Code to use the `past-behavior-interviews` skill by name.

Example prompts:

- "Use the past-behavior-interviews skill to rewrite these 10 interview questions so none of them mention our product or ask for predictions."
- "Here are my notes from five customer calls. Use past-behavior-interviews to classify each statement as behavior, commitment, or opinion and tell me what we actually learned."
