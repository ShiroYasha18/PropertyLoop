# crew_agents/tenancy_agent.py
from crewai import Agent
from langchain_core.tools import Tool
from tools.text_tools import extract_location

class TenancyAgentBuilder:
    @staticmethod
    def build(llm):
        """
        Build and return the Tenancy FAQ Agent
        """
        tenancy_expert_agent = Agent(
            role="Tenancy Law Specialist",
            goal="Provide accurate information about tenancy laws and rental processes",
            backstory="""You are a knowledgeable expert on tenant rights, rental agreements, 
            and landlord-tenant relationships. You have years of experience in real estate law
            and can provide guidance on common tenancy issues, explain relevant laws,
            and offer practical advice on navigating rental processes.""",
            verbose=True,
            llm=llm,
            tools=[
                Tool(
                    name="extract_location",
                    func=lambda text: extract_location(text, llm),
                    description="Extract location from text if mentioned"
                )
            ]
        )
        
        return tenancy_expert_agent
    
    @staticmethod
    def create_task(user_input):
        """
        Create a tenancy question task
        """
        return {
            "description": f"""
            Answer the following tenancy-related question:
            {user_input}
            
            First, check if a specific location is mentioned. If so, provide location-specific advice.
            If not, note that laws vary by location and provide general guidance that applies
            in most jurisdictions.
            
            Your response should:
            1. Directly address the user's question
            2. Explain relevant legal concepts in simple terms
            3. Suggest practical next steps if applicable
            4. Include any important disclaimers (e.g., "This is general advice, not legal counsel")
            
            Keep your response focused and helpful.
            """,
            "expected_output": "A helpful, accurate answer to the tenancy question with appropriate context and disclaimers"
        }