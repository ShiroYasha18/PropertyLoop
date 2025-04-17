# crew_agents/issue_agent.py
from crewai import Agent
from langchain_core.tools import Tool
from tools.image_tools import analyze_property_image

class IssueAgentBuilder:
    @staticmethod
    def build(llm, vision_llm):
        """
        Build and return the Issue Detection Agent
        """
        issue_detection_agent = Agent(
            role="Property Issue Detection Specialist",
            goal="Identify property issues from images and provide actionable troubleshooting advice",
            backstory="""You are an experienced property inspector with decades of 
            experience identifying issues in residential and commercial properties.
            After receiving an image, you first ask specific questions about the user's concerns
            before providing a detailed analysis. You maintain context of previous observations
            while addressing new questions about the same image.""",
            verbose=True,
            llm=llm,
            tools=[
                Tool(
                    name="analyze_property_image",
                    func=lambda image_data, query: analyze_property_image(image_data, query, vision_llm),
                    description="Analyze an image of a property to identify issues"
                )
            ]
        )
        
        return issue_detection_agent
    
    @staticmethod
    def create_task(image_data=None, user_input=None):
        if image_data:
            return {
                "description": """Please analyze this image for:
                - Water damage and moisture issues
                - Structural problems
                - Mold or environmental hazards
                - Safety concerns
                - Required repairs""",
                "context": [{"type": "image", "content": image_data}],
                "expected_output": "Direct analysis of visible property issues"
            }
        if image_data and not user_input:
            return {
                "description": """An image has been provided. Ask the user what specific aspects they would like examined:
                1. General property condition assessment
                2. Specific issue investigation (water damage, mold, structural)
                3. Safety hazard evaluation
                4. Repair priority assessment
                5. Cost estimation for repairs""",
                "context": [{"type": "image", "content": image_data, "description": "Property image for analysis", "expected_output": "User preference for analysis focus"}],
                "expected_output": "Clear question to user about their specific concerns with the property image"
            }
        context = []
        
        if user_input:
            context.append({
                "type": "text",
                "content": user_input,
                "description": "User query about property issues",
                "expected_output": "Analysis of the text query"
            })
        
        if image_data:
            context.append({
                "type": "image",
                "content": image_data,
                "description": "Analyze this image for property issues, damage, or maintenance problems",
                "expected_output": "Detailed visual analysis of property issues"
            })
        
        return {
            "description": """Examine the provided information to:
            1. Identify visible property issues or damage
            2. Assess the severity of the problems
            3. Suggest potential solutions or next steps
            4. Recommend if professional inspection is needed""",
            "context": context,
            "expected_output": """Detailed analysis including:
            - Problem identification
            - Severity assessment
            - Recommended actions
            - Safety concerns (if any)"""
        }
    
    def analyze_image(image_data):
        from groq import Groq
        import time
        
        client = Groq(api_key=api_key)
        max_retries = 3
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                completion = client.chat.completions.create(
                    model="meta-llama/llama-4-maverick-17b-128e-instruct",
                    messages=[
                        {
                            "role": "system",
                            "content": """You are an expert property inspector. Provide only factual observations and professional recommendations. 
                            Focus exclusively on:
                            - Precise damage descriptions
                            - Technical assessments
                            - Professional recommendations
                            - Safety implications
                            
                            Do not include any meta-commentary, thoughts about tasks, or personal reflections."""
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": """Property Inspection Report:

                                    1. Water Damage Assessment:
                                       - Location and extent
                                       - Active leak indicators
                                       - Source identification
                                       - Severity classification

                                    2. Structural Evaluation:
                                       - Wall/ceiling conditions
                                       - Structural integrity
                                       - Support system status

                                    3. Environmental Issues:
                                       - Mold/mildew presence
                                       - Moisture assessment
                                       - Air quality factors

                                    4. Safety Analysis:
                                       - Critical risks
                                       - Structural concerns
                                       - Health hazards

                                    5. Action Items:
                                       - Required interventions
                                       - Professional services needed
                                       - Priority level"""
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_data}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.1,
                    max_completion_tokens=2048,
                    top_p=1
                )
                return completion.choices[0].message.content
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    return f"Error analyzing image: {str(e)}"