# Five Principles for a Small Team

These five principles are the backbone of this kit. You do not need a big governance team to follow them. You need a short list, a named owner, and a weekly habit of checking it.

## 1. Trustworthy data and context

Your AI is only as good as the information it can see. If the data is stale, wrong, or mixed up, the answers will be too.

- List your main data sources in [templates/ai-inventory.csv](../templates/ai-inventory.csv) and mark which ones are trusted.
- Write one sentence for each key term your team uses, such as what "active user" means, and keep it where everyone can find it.
- Remove test data, old copies, and personal data from any source an agent can read.
- Check one data source each week for freshness and fix the oldest problem first.
- Give agents access to the clean source, not a random spreadsheet on someone's laptop.

## 2. Security and policy enforcement

Decide what is allowed before an agent runs, and make the rules hard to skip by accident.

- Write your rules down in [templates/acceptable-use-policy.md](../templates/acceptable-use-policy.md) and share them with the whole team.
- Give each person and each agent only the access they need for their own job.
- Use separate keys for each app or agent, and rotate any key that was shared in chat or email.
- Block agents from reading secrets, passwords, and private customer data unless that access is named in the policy.
- Test your rules with the policy checker in [tools/agov/](../tools/agov/) before you trust them.

## 3. Transparency and accountability

Someone should be able to explain what an agent did, why it did it, and who is responsible.

- Name one owner for every agent, model, and tool in your inventory.
- Log every agent action to JSONL with the action logger in [tools/agov/](../tools/agov/), including who asked, what tool ran, and what changed.
- Keep the logs in one place, and keep them long enough to check a problem from last week.
- When an agent gives a wrong or odd answer, save the prompt, the answer, and the source it used.
- Review the logs in your weekly review and ask: what would we tell a customer if this went wrong?

## 4. Operational oversight

Watch your AI while it runs, not only when something breaks.

- Run the checks in [templates/agent-runtime-checklist.md](../templates/agent-runtime-checklist.md) before any new agent goes live.
- Watch for repeat failures, slow tools, and agents that retry the same call again and again.
- Set a simple alert for errors and for spend that jumps suddenly.
- Keep a short list of known failures and what fixed them, so the next person does not repeat them.
- Pause an agent at the first sign of odd behavior. Restarting it is cheap. Cleaning up a bad run is not.

## 5. Cost optimization

Spend on purpose. Cut waste, not useful work.

- Tag every model call with the user, team, and app that caused it, so you can see who spent what.
- Set a monthly budget per team, an alert at 80 percent, and a hard limit that stops new calls.
- Use a cheaper model for simple jobs. Save the strongest model for hard jobs. See [02-cost.md](02-cost.md).
- Review your top three spenders every week and fix the biggest waste first.
- Remove models, agents, and tools nobody uses. Each one you keep still costs time to maintain.

## How to use this page

Pick one action from each principle this week. Do those five things, then repeat next week with the next five. Small steady fixes beat a big policy document nobody reads.
