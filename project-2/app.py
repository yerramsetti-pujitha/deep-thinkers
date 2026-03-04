import streamlit as st
from groq import Groq
import urllib.parse

# Set page configuration
st.set_page_config(page_title="Groq Chatbot", page_icon="⚡", layout="centered")

st.title("⚡ Fast Chatbot with Groq")
st.write("Powered by Streamlit and Groq's blazing fast inference API.")
st.markdown("**Pro Tip:** Type `/image [your prompt]` to generate an image!")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Settings")
    # Get API Key from user securely
    api_key = st.text_input("Enter your Groq API Key:", type="password", help="Get your API key from https://console.groq.com/keys")
    
    # Model selection dropdown
    selected_model = st.selectbox(
        "Choose a Model:",
        [
            "llama3-8b-8192", 
            "llama3-70b-8192", 
            "mixtral-8x7b-32768", 
            "gemma-7b-it"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("Build with ❤️ using Streamlit & Groq")

# --- Session State Initialization ---
# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") == "image":
            st.image(message["content"], caption=message.get("caption"))
        else:
            st.markdown(message["content"])

# --- Helper function for streaming ---
def parse_groq_stream(stream):
    """Generator to parse Groq's stream chunks and yield text."""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content

# --- Chat Input & Response Generation ---
if prompt := st.chat_input("Type a message or /image [prompt]..."):
    
    # Require API key before proceeding
    if not api_key:
        st.info("⚠️ Please enter your Groq API Key in the sidebar to start chatting.")
        st.stop()

    # 1. Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- IMAGE GENERATION LOGIC ---
    if prompt.strip().lower().startswith("/image"):
        # Extract the prompt for the image
        image_prompt = prompt[6:].strip()
        if not image_prompt:
            image_prompt = "A beautiful futuristic city" # fallback
            
        with st.chat_message("assistant"):
            with st.spinner("Generating image..."):
                # Using Pollinations AI for free, no-API-key image generation
                encoded_prompt = urllib.parse.quote(image_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                
                st.image(image_url, caption=image_prompt)
        
        # Save to session state
        st.session_state.messages.append({
            "role": "assistant", 
            "type": "image", 
            "content": image_url, 
            "caption": image_prompt
        })
        
    # --- TEXT GENERATION LOGIC (GROQ) ---
    else:
        # 2. Initialize Groq client
        client = Groq(api_key=api_key)

        # 3. Generate and stream the assistant's response
        with st.chat_message("assistant"):
            try:
                # Request streaming response from Groq
                # Only send text messages to Groq to avoid API errors
                groq_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages if m.get("type", "text") != "image"
                ]
                
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=groq_messages,
                    stream=True,
                )
                
                # Use Streamlit's built-in write_stream to display the text as it arrives
                response = st.write_stream(parse_groq_stream(stream))
                
                # Add the final full response to session state
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": response})
                
            except Exception as e:
                st.error(f"An error occurred: {e}")