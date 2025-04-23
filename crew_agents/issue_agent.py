# crew_agents/issue_agent.py
from crewai import Agent
from langchain_core.tools import Tool
from tools.image_tools import analyze_property_image

class IssueAgentBuilder:
    @staticmethod
    def build(llm, vision_llm, text_llm=None):
        """
        Build and return the Issue Detection Agent
        """
        issue_detection_agent = Agent(
            role="Property Issue Detection Specialist",
            goal="Identify property issues from images and text, providing actionable troubleshooting advice",
            backstory="""You are an experienced property inspector with decades of 
            experience identifying issues in residential and commercial properties.
            You can analyze both images and text queries to provide detailed property assessments.
            You maintain context of previous observations while addressing new questions.""",
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
        context = []
        
        # Add text input to context if provided
        if user_input:
            context.append({
                "type": "text",
                "content": user_input,
                "description": "User query about property issues",
                "expected_output": "Analysis of the text query"
            })
        
        # Add image data to context if provided
        if image_data:
            context.append({
                "type": "image",
                "content": image_data,
                "description": "Analyze this image for property issues, damage, or maintenance problems",
                "expected_output": "Detailed visual analysis of property issues"
            })
        
        # Determine the appropriate task description and model based on input types
        if image_data and user_input:
            # Case: Both image and text provided
            description = """Examine both the image and text query to:
            1. Identify visible property issues or damage
            2. Address specific concerns mentioned in the text
            3. Assess the severity of the problems
            4. Suggest potential solutions or next steps
            5. Recommend if professional inspection is needed"""
            
            expected_output = """Comprehensive analysis including:
            - Problem identification from both visual and textual information
            - Severity assessment
            - Recommended actions
            - Safety concerns (if any)"""
            
            model = "meta-llama/llama-4-maverick-17b-128e-instruct"  # Vision-capable model
            
        elif image_data and not user_input:
            # Case: Only image provided
            description = """Examine the provided image to:
            1. Identify visible property issues or damage
            2. Assess the severity of the problems
            3. Suggest potential solutions or next steps
            4. Recommend if professional inspection is needed"""
            
            expected_output = """Detailed visual analysis including:
            - Problem identification
            - Severity assessment
            - Recommended actions
            - Safety concerns (if any)"""
            
            model = "meta-llama/llama-4-maverick-17b-128e-instruct"  # Vision-capable model
            
        elif not image_data and user_input:
            # Case: Only text provided
            description = """Analyze the provided text query to:
            1. Identify potential property issues or concerns
            2. Provide recommendations based on the text query
            3. Suggest next steps or actions
            4. Offer relevant property maintenance advice"""
            
            expected_output = """Detailed analysis including:
            - Problem identification from text
            - Recommended actions
            - Any additional insights based on the text
            - Relevant property maintenance advice"""
            
            model = "meta-llama/llama-3.3-70b-versatile"  # Text-optimized model
            
        else:
            # Case: No input provided (fallback)
            description = """Please provide either a property image or a text query about property issues."""
            expected_output = "Prompt for user to provide input"
            model = "meta-llama/llama-3.3-70b-versatile"  # Default model
        
        return {
            "description": description,
            "context": context,
            "expected_output": expected_output,
            "model": model
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