from flask import Flask, request, jsonify
import google.generativeai as genai
import urllib.parse
import os

# Initialize Flask app to serve files from the current directory
app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    """Serve the main index.html file."""
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and API requests."""
    data = request.json
    user_message = data.get('message', '')
    api_key = data.get('api_key', '')
    history = data.get('history', [])

    # --- IMAGE GENERATION LOGIC ---
    if user_message.strip().lower().startswith('/image'):
        prompt = user_message[6:].strip() or "A cool futuristic landscape"
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
        return jsonify({"type": "image", "content": image_url, "caption": prompt})
    
    # --- TEXT GENERATION LOGIC (GEMINI) ---
    if not api_key:
        return jsonify({"type": "error", "content": "Please provide a Gemini API Key in the sidebar."}), 400

    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=api_key)
        
        # Use the recommended Gemini 1.5 Flash model for fast text tasks
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Format the history for Gemini (only text messages)
        formatted_history = []
        for msg in history:
            if msg.get('type') == 'text':
                role = "user" if msg['role'] == "user" else "model"
                formatted_history.append({"role": role, "parts": [msg['content']]})

        # Start chat session with history and send the new message
        chat_session = model.start_chat(history=formatted_history)
        response = chat_session.send_message(user_message)
        
        return jsonify({"type": "text", "content": response.text})
        
    except Exception as e:
        return jsonify({"type": "error", "content": f"Gemini API Error: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting server at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)