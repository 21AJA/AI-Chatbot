from flask import Flask, request, jsonify
import os
from flask_cors import CORS  # Allow frontend to communicate with backend
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set your Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=groq_api_key)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Use Groq API for chat completions
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_response = response.choices[0].message.content  # Correct response parsing

        return jsonify({"message": bot_response})

    except Exception as e:
        print("Error:", e)  # Debugging
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
