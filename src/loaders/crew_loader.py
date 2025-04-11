import yaml
from pathlib import Path
from typing import Literal, Type
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from crewai.tools import BaseTool
from typing import Union, Optional, Any
from loaders.provider_loader import get_llm_provider
from crewai_tools import DirectoryReadTool, FileReadTool


def parse_yaml(file_path: Path) -> Union[dict[str, Any], list, None]:
    with file_path.open('r') as f:
        return yaml.safe_load(f)


def create_agent(
    agent_cfg: dict[str, Any],
    tools: Optional[list[BaseTool]] = None,
) -> Agent:

    return Agent(
        role=agent_cfg["role"].strip(),
        goal=agent_cfg["goal"].strip(),
        backstory=agent_cfg.get("backstory", "").strip(),
        verbose=agent_cfg.get("verbose", False),
        max_iter=agent_cfg.get("max_iter", 10),
        tools=tools or [],
        llm=get_llm_provider(agent_cfg.get("llm", "gpt-4o")),
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


def get_tools(type: Literal["repo"], path: Path) -> list[BaseTool]:
    match type:
        case "repo":
            repo_tool = DirectoryReadTool(
                directory=str(path.cwd()),
                exclude_dirs=[".venv", ".git", "*/__pycache__", ".git", "node_modules"],
                exclude_files=["*.pyc", "*.log", "*.tmp", "*.sqlite3", "*.db"]
            )
            file_tool = FileReadTool()
            return [repo_tool, file_tool]
    return []


def construct_crew_from_config(type: Literal["repo"], config_dir: Path, verbose: bool = True) -> Crew:
    agents_config = parse_yaml(config_dir / "agents.yaml")
    tasks_config = parse_yaml(config_dir / "tasks.yaml")
    tools = get_tools(type, config_dir)
    agents = build_agents_dict(agents_config, tools)
    tasks = create_tasks_dict(tasks_config, agents)
    print("verbose", verbose)
    return Crew(
        agents=list(agents.values()),
        tasks=list(tasks.values()),
        verbose=verbose,
        output_log_file=True,
        memory=True,
        cache=True,
        manager_llm=ChatOpenAI(model="gpt-4")
    )
