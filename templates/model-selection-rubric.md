# Model Selection Rubric

Use this rubric when you need to pick a model for a task. Score each candidate model from 1 to 5 on every criterion, multiply each score by the criterion weight, and add the totals. The highest total wins, but read the notes before you commit: a model that fails on privacy or fallback availability should not win on quality alone.

| Criterion | Weight (1-5) | How to score (1-5) | Notes |
| --- | --- | --- | --- |
| Quality on your own task sample | 5 | 1 means most answers are wrong or unusable, 5 means answers are accurate and ready to use | Test on your own real examples, not on a vendor demo. Use at least 20 samples and keep the test set fixed so models are compared fairly. |
| Cost per 1k calls | 4 | 1 means far over budget, 5 means comfortably inside budget | Measure total cost per 1,000 real calls, including input tokens, output tokens, and any tool calls. Record the cost center it will charge. |
| Latency | 3 | 1 means too slow for the use case, 5 means fast enough with room to spare | Measure the 95th percentile response time under normal load, not a single best case run. |
| Data handling and privacy | 5 | 1 means data leaves your control with no clear terms, 5 means data handling meets your policy | Check where data is stored, whether it is used for training, how long it is kept, and whether the provider meets your data sensitivity rules. |
| Fallback availability | 4 | 1 means no backup if the model is down, 5 means a tested fallback is ready | Name a second model that can take over, confirm it is configured, and test the switch before you need it. |
| Ease of evaluation | 2 | 1 means results are hard to check, 5 means outputs are easy to verify | Prefer models whose outputs your team can review quickly, especially for customer facing work. |
| Vendor lock in | 2 | 1 means switching would be painful, 5 means switching is straightforward | Check whether prompts, tools, and data formats work with another provider with little rework. |

## How to use it

Pick the weights that fit your task and write them down before you score anything, so the scoring cannot be bent to favor a favorite. Score each model on the same sample and the same cost and latency measurements. Keep the filled in rubric with the decision, including the date and who scored it, so the choice can be reviewed later. Revisit the rubric when prices change, a new model appears, or the task changes.
