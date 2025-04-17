# crew_agents/router_agent.py
from crewai import Agent
from tools.text_tools import build_query_context

class RouterAgentBuilder:
    @staticmethod
    def build(llm):
        return Agent(
            role="Query Router",
            goal="Accurately categorize and route user queries to the right specialist agent",
            backstory="""You are an expert at understanding user intentions and determining 
            the appropriate specialist to handle their real estate questions. You excel at 
            analyzing both text and detecting when visual analysis is needed.""",
            verbose=True,
            llm=llm
        )
    
    @staticmethod
    def create_task(user_input, has_image=False, conversation_history=None):
        if conversation_history is None:
            conversation_history = []
            
        context = build_query_context(user_input, conversation_history)
        
        return {
            "description": f"""
            Determine which specialist should handle this query:
            {context}
            Has image: {'Yes' if has_image else 'No'}
            
            If the query is about property issues, maintenance problems, visual inspection,
            or if there's an image attached, respond with ONLY "issue_detection".
            
            If the query is about tenancy laws, rental agreements, landlord/tenant rights,
            or rental processes, respond with ONLY "tenancy_faq".
            
            If unclear, respond with ONLY "ask_clarification".
            
            Your response MUST be exactly one of these three options, with no additional text.
            """,
            "expected_output": "One of three options: 'issue_detection', 'tenancy_faq', or 'ask_clarification'"
        }
        