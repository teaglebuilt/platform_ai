import asyncio
from crewai import Crew, Agent, Task

# Create an agent with code execution enabled
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

# Create tasks that require code execution
task_1 = Task(
    description="Analyze the first dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent
)

task_2 = Task(
    description="Analyze the second dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent
)

research_crew = Crew(agents=[coding_agent], tasks=[task_1])


class ResearchService():
    async def process_task():
        async def async_crew_execution():
            result = await research_crew.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
            print("Crew Result:", result)