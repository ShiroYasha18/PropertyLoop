# main.py
import os
from typing import Dict, Any, Optional  # Add typing imports
from crewai import Crew, Task, Process
from langchain_groq import ChatGroq
from crew_agents.router_agent import RouterAgentBuilder
from crew_agents.issue_agent import IssueAgentBuilder
from crew_agents.tenancy_agent import TenancyAgentBuilder

class RealEstateAssistant:
    def __init__(self, api_key=None):
        # Set up API key
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key is required.")
        
        # Initialize LLM instances with specific models
        self.llm = ChatGroq(
            api_key=self.api_key,
            model_name="meta-llama/llama-4-maverick-17b-128e-instruct"  # Updated model
        )
        
        # Build agents
        self.router_agent = RouterAgentBuilder.build(self.llm)
        self.issue_agent = IssueAgentBuilder.build(self.llm, self.api_key)
        self.tenancy_agent = TenancyAgentBuilder.build(self.llm)
        
        # Initialize conversation memory
        self.conversation_history = []
    
    def process_query(self, user_input, image=None):
        """
        Process a user query through the multi-agent system
        
        Args:
            user_input (str): User's text query
            image (str, optional): Base64 encoded image data
            
        Returns:
            str: Response from the appropriate agent
        """
        # Track conversation
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Determine if there's an image
        has_image = image is not None
        
        # Create routing task
        routing_task_spec = RouterAgentBuilder.create_task(user_input, has_image)
        routing_task = Task(
            description=routing_task_spec["description"],
            agent=self.router_agent,
            expected_output=routing_task_spec["expected_output"]
        )
        
        # Execute routing task
        routing_crew = Crew(
            agents=[self.router_agent],
            tasks=[routing_task],
            verbose=True,
            process=Process.sequential
        )
        
        try:
            # Get routing result
            route_result = routing_crew.kickoff()
            agent_type = route_result.lower().strip()
            
            # Process based on agent type
            if agent_type == "issue_detection":
                if has_image:
                    # Create and execute issue detection task
                    issue_task_spec = IssueAgentBuilder.create_task(image, user_input)
                    issue_task = Task(
                        description=issue_task_spec["description"],
                        agent=self.issue_agent,
                        context=[{
                            "description": "Property Issue Analysis",
                            "content": image,
                            "expected_output": "Visual analysis of property issues",
                            "type": "image_analysis"
                        }],
                        expected_output=issue_task_spec["expected_output"]
                    )
                    
                    issue_crew = Crew(
                        agents=[self.issue_agent],
                        tasks=[issue_task],
                        verbose=True,
                        process=Process.sequential
                    )
                    
                    response = issue_crew.kickoff()
                else:
                    response = "To help identify property issues, please upload an image of the problem area."
                    
            elif agent_type == "tenancy_faq":
                # Create and execute tenancy question task
                tenancy_task_spec = TenancyAgentBuilder.create_task(user_input)
                tenancy_task = Task(
                    description=tenancy_task_spec["description"],
                    agent=self.tenancy_agent,
                    expected_output=tenancy_task_spec["expected_output"]
                )
                
                tenancy_crew = Crew(
                    agents=[self.tenancy_agent],
                    tasks=[tenancy_task],
                    verbose=True,
                    process=Process.sequential
                )
                
                response = tenancy_crew.kickoff()
                
            else:  # ask_clarification
                response = """I'm not sure if you're asking about:
                1. A physical property issue (please upload an image if applicable)
                2. Tenancy or rental agreement questions
                
                Could you please clarify?"""
                
        except Exception as e:
            response = f"I encountered an error while processing your request. Please try again. Error: {str(e)}"
        
        # Track response
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
    
    def _create_task(self, task_dict: Dict[str, Any]) -> Task:
        return Task(
            description=task_dict["description"],
            context=task_dict.get("context", []),  # Accept the list of context dictionaries
            expected_output=task_dict["expected_output"]
        )