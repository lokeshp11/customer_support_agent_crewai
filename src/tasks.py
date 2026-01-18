from crewai import Task

class CustomerSupportTasks:
    def intent_classification_task(self, agent, customer_query):
        return Task(
            description=f'Analyze the following customer query and classify it: Billing, Technical Support, Refund, Account, General, or Out of Scope.\nAlso extract any user identifier (Name, Email) if mentioned.\n\nQuery: "{customer_query}"',
            expected_output='The category of the query and extracted user ID (e.g., "Category: Billing, User: John Doe").',
            agent=agent
        )

    def retrieval_task(self, agent, customer_query):
        return Task(
            description=f'Use "User Details Tool" if a user IP is found. Use "Policy Search Tool" to find relevant info for the query: "{customer_query}".\nFind policies, plan details, or troubleshooting steps.',
            expected_output='A summary of the User Profile (if found) AND relevant policy/product documents. Return "None" if nothing relevant is found.',
            agent=agent
        )

    def response_generation_task(self, agent, customer_query):
        return Task(
            description=f'''Draft a response to: "{customer_query}".
            1. Personalize: If user found, address them by name and ONLY mention their plan name.
            2. New User: If identifier provided but not found in DB, welcome them as a potential new customer and guide them to our Plans.
            3. Answer: Use retrieved Policy/Product info to solve their query.
            4. Ticket: If valid query but no info found, generate Ticket #.
            5. Out of Scope: Polite rejection.
            6. MINIMALISM: Do NOT include account details like price, address, or dates unless specifically asked for.
            ''',
            expected_output='A final response to the user.',
            agent=agent
        )

    def quality_assurance_task(self, agent):
        return Task(
            description='Review the drafted response. Check for:\n1. Policy violations.\n2. Missing disclaimers.\n3. Accuracy.\n4. PRIVACY: Ensure NO account details (price, dates, address) are leaked unless the user asked for them. Only the Plan Name is allowed for verification.\nIf the response is compliant, output "Approved". If not, correct it and output the corrected response.',
            expected_output='Final verified response text (or corrected version).',
            agent=agent
        )

    def tone_optimization_task(self, agent):
        return Task(
            description='Review the verified response and optimize its tone. It should be polite, professional, and empathetic. Do not change the factual details.',
            expected_output='The final, polished response ready to be sent to the customer.',
            agent=agent
        )
