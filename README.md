# Real Estate Assistant

Welcome to the Real Estate Assistant project! This application leverages AI-powered agents to analyze property images and provide actionable insights. It is designed to assist property inspectors and real estate professionals in identifying issues and recommending solutions.

## Features

- **Property Issue Detection**: Analyze images to identify water damage, structural problems, mold, and other environmental hazards.
- **Interactive Query Handling**: Engage with users to understand their specific concerns and tailor the analysis accordingly.
- **Professional Recommendations**: Provide detailed reports with technical assessments and safety implications.

## Technology Stack

- **CrewAI**: For multi-agent orchestration and task management.
- **Groq LLMs**: Utilized for natural language processing and image analysis.
- **Streamlit**: For building the user interface and interaction.

## Agents and Tools

### Issue Detection Agent

![Issue Detection Agent](assets/images/issue_detection_agent.png)

- **Role**: Property Issue Detection Specialist
- **Goal**: Identify property issues from images and provide actionable troubleshooting advice.
- **Tools Used**:
  - **Image Analysis**: Uses `analyze_property_image` from `tools.image_tools` to identify issues such as water damage, mold, and structural problems.
  - **Language Model**: Utilizes Groq's LLMs for generating detailed inspection reports.

### Router Agent

- **Role**: Query Router
- **Goal**: Accurately categorize and route user queries to the right specialist agent.
- **Tools Used**:
  - **Text Analysis**: Uses `build_query_context` from `tools.text_tools` to understand user intentions and determine the appropriate specialist.

## About Groq

Groq is a leading provider of AI and machine learning solutions, offering powerful language models that enable advanced natural language processing and image analysis. Their models are designed to deliver high performance and accuracy, making them ideal for applications in real estate and property inspection.

### Obtaining a Groq API Key

To use Groq's LLMs, you need an API key. Follow these steps to obtain one:

1. **Sign Up**: Visit [Groq's website](https://groq.com) and create an account.
2. **API Access**: Navigate to the API section in your account dashboard.
3. **Generate Key**: Follow the instructions to generate a new API key.
4. **Secure Your Key**: Store the key securely and add it to your `.env` file as shown above.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Streamlit
- Groq API Key

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ShiroYasha18/PropertyLoop.git
   cd PropertyLoop/real-estate-assistant

2. ```bash
   pip install -r requirements.txt
    ```
3. Set Up Environment Variables :
   Create a .env file in the root directory and add your Groq API key:
   
   ```plaintext
   GROQ_API_KEY="your_groq_api_key_here"
    ```
### Running the Application
1. Start the Streamlit App :
   
   ```bash
   streamlit run app.py
    ```
2. Access the Application :
   Open your browser and navigate to http://localhost:8501 .

## Demo

### Image Analysis
![Property Issue Detection](demo_pics/image-analysis.jpg)
*Example of image analysis identifying water damage and structural issues*

### Text Query Handling
![Tenancy Advice](demo_pics/text-query.jpg)
*Example of text-based query about rental agreements*