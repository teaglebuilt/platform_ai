This will be a central library and platform for ai management.

There are two use cases to start with.

1. **Repo based AI feature**
  Each repo will have a folder in `.github/config` with `agents.yaml` and `tasks.yaml`. It should train and understand the contents of everything in the codebase / repository. I can use `run feature --type repo --path ...` to manually trigger the crew. I can control the output based on `.github/prompts/objective.md`. Then i want to consider persistence and a webhook to retrain when new files or content has been added to the repo (via github webhook)

1. **Design Pattern**
  Use a hexagonal design pattern to work across many different integrations, providers, etc...

2. **How to use it**

  - **Repo Based AI Feature**
      Each repo will have a folder in `.github/config` with `agents.yaml` and `tasks.yaml`. It should train and understand the contents of everything in the codebase / repository. I can use `run feature --type repo --path ...` to manually trigger the crew. I can control the output based on `.github/prompts/objective.md`. Then i want to consider persistence and a webhook to retrain when new files or content has been added to the repo (via github webhook)
  
  - Use with [continue.dev](https://www.continue.dev/). I want to use auto completion, chat, mcp protocol.

3. **Scheduled Jobs**
    I want to run things on a schedule to scrape content to train models and agents. I want to use an rss feed to centralize results. I use n8n on kubernetes already so determine how we should use it. 

    Want to build gen ai solutions.


4. **Architecture Design**
    Ollama is already on kubernetes connected to a gpu. An ai gateway is already deployed that we will communicate directly with which will proxy between external providers like openai, etc...

    What else do we need to support the different capabilities? Databases? etc...



Finally, consider the existing codebase with the content in this file and determine a path forward.
