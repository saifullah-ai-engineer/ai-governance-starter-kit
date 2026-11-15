# Choice: Pick the Right Model for Each Job

## Why one model is not enough

Models differ. One may write better code. Another may summarize faster. Another may cost far less for simple answers. The best model today may not be the best one next quarter, because new models arrive often and prices change.

If you standardize on a single model, you pay for strength you do not need on easy tasks, and you get stuck when that model has an outage, a price rise, or a better rival. A small approved set gives you options without chaos.

Keep the set small: two or three models is enough for most small teams. One strong model for hard work, one cheaper model for routine work, and optionally one specialist for a key task such as code.

## How to compare models on a small task set

Do not trust a leaderboard alone. Test models on your own tasks, with your own data.

1. Pick 10 to 20 real tasks from your work. Include easy, medium, and hard ones. Use real prompts, not made-up examples.
2. Write down what a good answer looks like for each task before you run the test.
3. Run the same tasks through each candidate model with the same prompts and the same settings.
4. Score each answer with [templates/model-selection-rubric.md](../templates/model-selection-rubric.md). Score quality, speed, cost per task, and how often it follows your format.
5. Note failures by hand: wrong facts, broken code, missing steps, or unsafe output.
6. Pick the winner for each task type, not one winner for everything. Record the choice and the date.

Repeat the test when a new model looks promising or when your tasks change. Keep the old task set so results stay comparable.

## Fallback and substitution

Plan for the day a model is down, slow, or too expensive. Your app should keep working.

- **Keep model names in config, not code.** Put the model name, the provider, and the routing rule in one config file. Changing a model should be a one-line edit, not a code change.
- **Name a fallback for each task.** If the main model fails or times out, send the request to the next model on the list. Test the fallback once a month.
- **Keep prompts portable.** Avoid tricks that only work on one model. If a prompt only works with one provider, note that in the config.
- **Do not hard-code provider keys in code.** Use one place for keys and access, so a key change does not touch every app.
- **Shift traffic slowly.** When you switch models, send a small share of traffic first, watch the results for a day, then move the rest.

## Quarterly model review

Book one hour every three months. Bring the rubric scores, the cost numbers from [02-cost.md](02-cost.md), and any failures from your logs.

1. Check each model in use: is it still the best fit for its tasks, or has a cheaper rival caught up?
2. Look at new models released since the last review. Test only the ones that fit a real need.
3. Retire models nobody uses. Remove them from config and from [templates/ai-inventory.csv](../templates/ai-inventory.csv).
4. Update the approved list and tell the team what changed and why.
5. Update the fallback list at the same time, so a switch stays a config change.

The goal is simple: the best model for the job should be the default, and switching to it should be easy.
