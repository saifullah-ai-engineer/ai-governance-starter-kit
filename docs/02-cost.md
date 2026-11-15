# Cost: Keep AI Spend Under Control

## How AI spend works

Most AI providers charge by tokens, which are small chunks of text. You pay for the text you send in and the text the model sends back. Long prompts, long answers, and long chat histories all cost more.

Agents multiply the cost. One user request can turn into many model calls: the agent plans, calls a tool, reads the result, plans again, and repeats. A coding agent can do this for hours. A loop that retries a failing tool can burn through a budget in minutes.

So do not estimate cost per user request. Estimate cost per full agent run, including retries and tool calls.

## Attribute spend: know who spent what

You cannot control spend you cannot see. Tag every call with at least these four labels: user, team, app or agent, and task. If your provider does not support tags, add them in your own logs.

Steps:

1. List each agent and app in [templates/ai-inventory.csv](../templates/ai-inventory.csv) with its owner.
2. Add a cost label to each one, such as `team: support` and `agent: triage`.
3. Pull a spend report from your provider once a week and group it by those labels.
4. Run the cost estimator in [tools/agov/](../tools/agov/) on a typical task for each agent, so you know the normal cost before you see a surprise bill.
5. Share the numbers with the team. People spend less when they can see their own usage.

## Budgets, alerts, and hard limits

Set three layers. Each one catches problems the last one missed.

1. **Budget:** a monthly amount per team or per app. Start with last month's spend plus a small margin.
2. **Alert:** a notice at 80 percent of budget, sent to the owner and the team lead. At this point, look for waste before you spend more.
3. **Hard limit:** a stop that blocks new calls when the budget is used up. Use this for experiments, demos, and any agent that can loop.

Do not set one limit for everyone. A support agent that runs all day needs a higher limit than a weekly report agent. Give the limit to the owner, not to the whole company.

Start with visibility before strict limits. If you block everything on day one, your team will work around you. Show the numbers first, agree the budgets, then turn on the hard limits.

## Routing: use a cheaper model for simple tasks

Not every task needs your strongest, most expensive model. A short summary, a simple classification, or a first draft can often use a cheaper model with no visible loss in quality.

Steps:

1. Sort your tasks into simple, medium, and hard. Simple means short, clear, and low risk if the answer is slightly off.
2. Pick a cheaper model for simple tasks and test it on 10 real examples. Compare the answers by hand.
3. If the cheaper model passes, route simple tasks to it by default. Keep the strong model for hard tasks.
4. Put the routing rule in config, so you can change it without editing code. See [03-choice.md](03-choice.md).
5. Check the savings after one week. If quality drops, move that task back to the stronger model.

Watch out for hidden costs: a cheap model that needs three retries is not cheap. Count the full run, not one call.

## Weekly cost review routine

Book 30 minutes, same time each week, with the agent owners.

1. Open last week's spend by team, app, and agent.
2. Name the top three spenders and the top three changes from the week before.
3. For each one, ask: was this useful work, a retry loop, or a bug?
4. Fix the biggest waste first. Common fixes: shorten the prompt, trim old chat history, stop retrying a failing tool, or move a simple task to a cheaper model.
5. Update the budgets if a real workload grew, and write the decision in [templates/risk-register.csv](../templates/risk-register.csv) if the risk changed.
6. Remove any agent or model with zero use in the last 30 days.

Keep the review short. If you cannot explain a spike in two minutes, log it as an action and move on.
