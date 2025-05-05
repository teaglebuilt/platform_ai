from typing import Optional, Any, Literal
from pathlib import Path
from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from crewai_tools import FileReadTool
from platform_ai.infra.frameworks.crewai.tools.repo_reader import LocalRepoReaderTool
from platform_ai.utilities.io import parse_yaml
from platform_ai.infra.providers.registry import get_llm_provider


def create_agent(
    agent_cfg: dict[str, Any],
    tools: Optional[list[BaseTool]] = None,
) -> Agent:
    llm_provider = get_llm_provider(agent_cfg.get("llm", "gpt-4o"))
    llm = LLM(model=llm_provider.model_name, base_url=llm_provider.host_url)

    return Agent(
        role=agent_cfg["role"].strip(),
        goal=agent_cfg["goal"].strip(),
        backstory=agent_cfg.get("backstory", "").strip(),
        verbose=agent_cfg.get("verbose", False),
        max_iter=agent_cfg.get("max_iter", 10),
        tools=tools or [],
        llm=llm,
        system_template=agent_cfg.get("system_template", ""),
        prompt_template=agent_cfg.get("prompt_template", ""),
        response_template=agent_cfg.get("response_template", ""),
    )


def create_task(task_cfg: dict[str, Any], agents_dict: dict[str, Agent]) -> Task:
    agent_name = task_cfg["agent"]
    assigned_agent = agents_dict.get(agent_name)
    if not assigned_agent:
        raise ValueError(f"Agent '{agent_name}' is not defined in agents.yaml.")

    return Task(
        description=task_cfg["description"],
        agent=assigned_agent,
        expected_output=task_cfg.get("expected_output", "")
    )


def build_agents_dict(agents_config, tools) -> dict[str, Agent]:
    agents_dict = {}

    if isinstance(agents_config, dict):
        for agent_key, agent_cfg in agents_config.items():
            agents_dict[agent_key] = create_agent(agent_cfg, tools)

    elif isinstance(agents_config, list):
        for agent_item in agents_config:
            for agent_key, agent_cfg in agent_item.items():
                agents_dict[agent_key] = create_agent(agent_cfg, tools)
    else:
        raise ValueError("agents.yaml format is invalid. Must be dict or list of dicts.")

    return agents_dict


def create_tasks_dict(tasks_config, agents_config) -> dict[str, Task]:
    tasks_dict = {}

    if isinstance(tasks_config, dict):
        for task_key, task_cfg in tasks_config.items():
            tasks_dict[task_key] = create_task(task_cfg, agents_config)

    elif isinstance(tasks_config, list):
        for task_item in tasks_config:
            for task_key, task_cfg in task_item.items():
                tasks_dict[task_key] = create_task(task_cfg, agents_config)

    return tasks_dict


def get_tools(type: Literal["repo", "local"]) -> list[BaseTool]:
    match type:
        case "repo":
            repo_tool = LocalRepoReaderTool(directory=str(Path.cwd()))
            file_tool = FileReadTool()
            return [repo_tool, file_tool]
    return []


def construct_crew_from_config(
    type: Literal["repo", "local"],
    tools: list[BaseTool],
    config_dir: Path,
    verbose: bool = True
) -> Crew:
    agents_config = parse_yaml(config_dir / "agents.yaml")
    tasks_config = parse_yaml(config_dir / "tasks.yaml")
    tools = tools if not tools else get_tools(type)
    agents = build_agents_dict(agents_config, tools)
    tasks = create_tasks_dict(tasks_config, agents)

    return Crew(
        agents=list(agents.values()),
        tasks=list(tasks.values()),
        verbose=verbose,
        output_log_file=True,
        memory=True,
        cache=True,
        prompt_file=None if type == "repo" else ".github/prompts/objective.md",
        # manager_llm=ChatOllama(
        #     model="deepseek-coder-v2:latest",
        #     base_url="http://ollama.homelab.internal"
        # )
    )
