# tools/image_tools.py
from groq import Groq
import base64

def analyze_property_image(image_data: str, query: str, api_key: str) -> str:
    """
    Analyze property image using Groq's VLM
    """
    client = Groq(api_key=api_key)
    
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Analyze this property image and identify:
                            1. Any visible damage or issues
                            2. Severity of problems
                            3. Potential causes
                            4. Recommended solutions
                            
                            Additional context: {query}"""
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
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            stream=False
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error analyzing image: {str(e)}"
