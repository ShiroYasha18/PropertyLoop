from crewai import Agent
from langchain_core.tools import Tool
from tools.image_tools import analyze_property_image

class IssueAgentBuilder:
    @staticmethod
    def build(llm, api_key):
        def analyze_image(image_data):
            from groq import Groq
            
            client = Groq(api_key=api_key)
            try:
                completion = client.chat.completions.create(
                    model="meta-llama/llama-4-maverick-17b-128e-instruct",  # Updated model
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional property inspector. Analyze the image and provide specific details about visible damage and issues."
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Analyze this image and describe:\n1. Visible damage (water damage, mold, etc.)\n2. Structural issues\n3. Maintenance problems\n4. Safety hazards"
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
                    temperature=0.3,  # Lower temperature for more focused responses
                    max_completion_tokens=2048,
                    top_p=1
                )
                return completion.choices[0].message.content
            except Exception as e:
                return f"Error in image analysis: {str(e)}"

        return Agent(
            role="Property Issue Detection Specialist",
            goal="Analyze property images and provide detailed assessment of issues",
            backstory="""You are an expert property inspector with extensive experience in identifying 
            structural issues, water damage, mold, and safety hazards. You must use the image analysis 
            tool for every inspection and provide specific details about what you observe.""",
            verbose=True,
            llm=llm,
            tools=[
                Tool(
                    name="analyze_property_image",
                    func=analyze_image,
                    description="Use this tool to analyze the property image"
                )
            ],
            allow_delegation=False  # Prevent delegation to ensure tool usage
        )
    
    @staticmethod
    def create_task(image_data=None, user_input=None):
        return {
            "description": """Use the analyze_property_image tool to examine the image and provide:
            1. Detailed description of visible damage and issues
            2. Severity assessment of each problem
            3. Specific recommendations for repairs
            4. Safety concerns that need immediate attention""",
            "context": image_data,
            "expected_output": "A comprehensive analysis of the property issues based on the image"
        }