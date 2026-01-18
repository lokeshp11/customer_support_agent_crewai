from crewai import Agent
from langchain_openai import ChatOpenAI
from src.tools import policy_search_tool, fetch_user_details
from src.logger import setup_logging

logger = setup_logging()

class CustomerSupportAgents:
    def __init__(self):
        try:
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
            logger.info("Initialized ChatOpenAI LLM")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise e

    def intent_classification_agent(self):
        return Agent(
            role='Intent Classification Specialist',
            goal='Identify the category of the customer query and extract user identity if present',
            backstory='You are an expert at understanding customer intent. You categorize queries into: Billing, Technical Support, Refund & Cancellation, Account Management, General Inquiry, or Out of Scope. You also check if the user is providing their name or email (e.g., "I am John Doe"). If the user implies they are an existing customer but provides NO name/email, you must flag this.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def rag_retrieval_agent(self):
        return Agent(
            role='Information Retrieval Specialist',
            goal='Fetch relevant information from the Knowledge Base and User Database',
            backstory='You are responsible for finding verified information. 1. If the user identified themselves, use "User Details Tool" to fetch their profile. 2. Use "Policy Search Tool" to find answers to their specific question from the knowledge base. You consolidate all found data.',
            tools=[policy_search_tool, fetch_user_details],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def response_generation_agent(self):
        return Agent(
            role='Customer Support Representative',
            goal='Generate a helpful and accurate response based on retrieved information',
            backstory='''You craft clear, concise, and accurate answers for customers (PulseAI from Pulse Telecom).
            RULES:
            1. SCOPE: If "Out of Scope", politely decline.
            2. IDENTITY CHECK: CRITICAL - Upon the VERY FIRST interaction (e.g. initial greeting or first question), if the user has not provided their Name and Email, you MUST ask: "Are you an existing customer? If so, please share your Name and Email so I can access your account." Do NOT validate account info without this.
            3. USAGE: If user details were retrieved successfully, ALWAYS use them BUT only state the **Plan Name** (e.g. "I see you have the Pulse Home Basic plan"). DO NOT reveal price, renewal date, bill amount, or address unless the user SPECIFICALLY asks for those details. Be terse.
            4. NEW USER: If user provided a name but "User not found" was returned, treat them as a new customer.
            5. TICKET: If query is valid but no info found in docs, generate ticket.
            6. CLOSING: If the user says they have no more questions or ends the chat, conclude politely and append the token [CLOSE_CHAT] to the end of your response.
            ''',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def quality_assurance_agent(self):
        return Agent(
            role='Compliance & Quality Officer',
            goal='Validate the response for policy compliance and accuracy',
            backstory='You ensure that all customer communications are safe, accurate, and compliant with company policies. You reject any promises that violate rules. You explicitly ALLOW asking for Name and Email for verification purposes. CRITICAL: Ensure the representative ONLY mentions the plan name when identifying a user; you must reject responses that dump full profiles (billing dates, prices, etc) unless specifically requested.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def tone_optimization_agent(self):
        return Agent(
            role='Tone & Empathy Specialist',
            goal='Refine the response to be polite, professional, and empathetic',
            backstory='You polish communications to ensure they sound human, caring, and professional. You do not change the factual meaning, only the tone. IMPORTANT: Do NOT add signatures like "Warm regards", "Best", or "Pulse Telecom Support Team" to every message. Only use a signature if the conversation is clearly ending. Preserve the [CLOSE_CHAT] token if present at the end.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
