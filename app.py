# app.py
import streamlit as st
from PIL import Image
import io
import base64
import os
from main import RealEstateAssistant
from utils.helpers import format_response, check_image_size

# Set page config with the logo
st.set_page_config(
    page_title="PropertyLoop Assistant",
    page_icon="🏠",
    layout="wide"
)

# Display logo in the sidebar
logo = Image.open("assets/propertyloop-logo.png")
st.sidebar.image(logo, width=200)

# Initialize session state
if "assistant" not in st.session_state:
    st.session_state.assistant = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False

# Main UI
st.title("🏠 Real Estate Multi-Agent Assistant")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("""
    This assistant uses Crew AI to power two specialized agents:
    - 📸 **Issue Detection Agent**: Upload images of property problems for analysis
    - 📝 **Tenancy FAQ Agent**: Ask questions about rental laws and processes
    """)
    
    # Add Groq API key input
    api_key = st.text_input("Enter Groq API Key", type="password")
    if api_key and not st.session_state.api_key_set:
        try:
            # Initialize assistant with API key
            st.session_state.assistant = RealEstateAssistant(api_key=api_key)
            st.session_state.api_key_set = True
            st.success("API key set successfully!")
        except Exception as e:
            st.error(f"Error initializing assistant: {str(e)}")
    
    # Add information about the system
    st.subheader("How it works")
    st.write("""
    1. Upload an image for property issue detection
    2. Ask questions about tenancy and rental processes
    3. Our AI agents will analyze and respond appropriately
    """)
    
    # Add limitations information
    with st.expander("System Limitations"):
        st.write("""
        - Vision detection works best with clear, well-lit images
        - Tenancy advice is informational only, not legal counsel
        - Response time may vary based on query complexity
        - Knowledge of laws may not reflect recent changes
        """)

# Check if API key is set
if not st.session_state.api_key_set:
    st.info("Please enter your Groq API key in the sidebar to begin.")
    st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "image_analysis" in message and message["image"] is not None:
            # Display original image with analysis
            st.image(message["image"], width=300)
            st.write(format_response(message["content"]))
        else:
            st.write(format_response(message["content"]))

# User input
user_input = st.chat_input("Ask about property issues or tenancy questions...")
uploaded_file = st.file_uploader("Upload an image of property issue (optional)", type=["jpg", "jpeg", "png"])

# Process input
if user_input or uploaded_file:
    # Add user message to chat
    image_data = None
    image = None
    
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            
            # Check image size
            if not check_image_size(image):
                st.warning("Image is too large. Resizing for optimal processing.")
                image = image.resize((800, int(800 * image.height / image.width)))
            
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format if image.format else "JPEG")
            image_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            
            # Display user message with image
            with st.chat_message("user"):
                if user_input:
                    st.write(user_input)
                st.image(image, width=300)
                
            st.session_state.messages.append({
                "role": "user",
                "content": user_input if user_input else "Please analyze this image.",
                "image": image
            })
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            st.stop()
    elif user_input:
        # Text-only user message
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process with multi-agent system
    with st.chat_message("assistant"):
        with st.spinner("Our agents are analyzing your request..."):
            try:
                response = st.session_state.assistant.process_query(
                    user_input if user_input else "Analyze this image", 
                    image_data
                )
                
                # Add assistant message to chat
                if uploaded_file:
                    st.image(image, width=300)
                    st.write(format_response(response))
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "image": image,
                        "image_analysis": True
                    })
                else:
                    st.write(format_response(response))
                    st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_message = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})