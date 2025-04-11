This will be a central library and platform for ai management.

There are two use cases to start with.

1. **Repo based AI feature**
  Each repo will have a folder in `.github/config` with `agents.yaml` and `tasks.yaml`. It should train and understand the contents of everything in the codebase / repository. I can use `run feature --type repo --path ...` to manually trigger the crew. I can control the output based on `.github/prompts/objective.md`. Then i want to consider persistence and a webhook to retrain when new files or content has been added to the repo (via github webhook)