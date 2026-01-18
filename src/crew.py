from crewai import Crew, Process
from src.agents import CustomerSupportAgents
from src.tasks import CustomerSupportTasks
from src.tools import PolicyKnowledgeBase
from src.logger import setup_logging

logger = setup_logging()

class CustomerSupportCrew:
    def __init__(self, query):
        self.query = query

    def run(self):
        logger.info(f"Starting CustomerSupportCrew with query: {self.query}")
        try:
            # Initialize Knowledge Base
            PolicyKnowledgeBase.initialize()
            
            agents = CustomerSupportAgents()
            tasks = CustomerSupportTasks()

            # Create Agents
            intent_agent = agents.intent_classification_agent()
            retrieval_agent = agents.rag_retrieval_agent()
            gen_agent = agents.response_generation_agent()
            qa_agent = agents.quality_assurance_agent()
            tone_agent = agents.tone_optimization_agent()

            # Create Tasks
            task1 = tasks.intent_classification_task(intent_agent, self.query)
            task2 = tasks.retrieval_task(retrieval_agent, self.query)
            task3 = tasks.response_generation_task(gen_agent, self.query)
            task4 = tasks.quality_assurance_task(qa_agent)
            task5 = tasks.tone_optimization_task(tone_agent)

            # Create Crew
            crew = Crew(
                agents=[intent_agent, retrieval_agent, gen_agent, qa_agent, tone_agent],
                tasks=[task1, task2, task3, task4, task5],
                verbose=True,
                process=Process.sequential
            )

            result = crew.kickoff()
            logger.info("Crew execution completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error executing crew: {e}")
            raise e
