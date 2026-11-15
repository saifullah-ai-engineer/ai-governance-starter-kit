# Agent Runtime Checklist

Complete every item before an agent runs in production. If any item is not checked, the agent stays in a test environment.

## Identity

- [ ] The agent has a name and a short description of what it does
- [ ] The agent has a named human owner who is responsible for it
- [ ] The agent runs under its own identity, not a shared personal account

## Allowed tools

- [ ] Every tool the agent may call is listed by name
- [ ] Each tool has a clear purpose and a stated limit on what it can do
- [ ] Tools that can change data, send messages, or spend money are marked as write tools
- [ ] The agent cannot reach any tool that is not on the list

## Data sensitivity

- [ ] The highest data sensitivity the agent touches is recorded (public, internal, confidential, or restricted)
- [ ] The agent only receives the data it needs for its task, nothing more
- [ ] Personal data, credentials, and payment details are blocked before they reach the model
- [ ] The dataset or source the agent reads from is listed in the AI inventory

## Approval rules for writes

- [ ] Read only actions run without approval
- [ ] Every write action needs human approval, or a written rule that says which writes are safe to run alone
- [ ] The approval rule names who approves and how the approval is recorded
- [ ] The agent cannot deploy code, delete data, or contact a customer without approval

## Cost budget

- [ ] The agent has a monthly cost budget in USD
- [ ] The cost center that pays for it is recorded in the AI inventory
- [ ] An alert fires at 80 percent of the budget
- [ ] There is a hard cap that stops the agent if the budget is exceeded

## Logging

- [ ] Logging is turned on for every prompt, tool call, and result
- [ ] Logs record who or what triggered the run, what the agent did, and when
- [ ] Logs are kept for the agreed retention period and are readable by the owner
- [ ] A failed or unusual run can be found in the logs without guessing

## Fallback model

- [ ] A fallback model is named in case the main model is unavailable
- [ ] The fallback is configured and has been tested at least once
- [ ] The agent degrades gracefully, for example by telling the user, instead of failing silently

## Kill switch

- [ ] There is a documented way to stop the agent immediately
- [ ] At least two people know how to use the kill switch
- [ ] Stopping the agent leaves no half finished writes behind, or the cleanup steps are written down

## Owner sign off

- [ ] The owner has reviewed this checklist and signed off
- [ ] The agent is recorded in the AI inventory with status active
- [ ] A review date is set for the next check of this agent

Date completed: _______________
Owner: _______________
Reviewer: _______________
