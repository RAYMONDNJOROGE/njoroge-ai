from flask import Flask, render_template, request, session
from google import genai
from google.genai import types
import os

app = Flask(__name__)
app.secret_key = "85e6e50d53d4cfe9a5bb1460fc82c1d6514627521de6b94c84592a8e028e9e8d"

client = genai.Client(api_key="AIzaSyAPVZ4hCgLn4dxmqhTvPoMF10A1ASh0DpU")
model = "gemini-2.5-flash"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("prompt", "").strip()

    if not question:
        return "No prompt provided.", 400, {"Content-Type": "text/plain"}

    # Load or initialize chat history
    chat_history = session.get("chat_history", [])

    # Add user's current question to history
    chat_history.append({
        "role": "user",
        "text": question
    })

    # Build the conversation content
    contents = [
        types.Content(role=entry["role"], parts=[types.Part.from_text(entry["text"])])
        for entry in chat_history
    ]

    config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        system_instruction=[
            types.Part.from_text(
                text="I am Njoroge A.I., a helpful assistant that helps you in your learning. "
                     "When asked your name, always respond with: 'I am Njoroge A.I., a helpful assistant that helps you in your A.I needs straight outa Nairobi, Kenya.' "
                     "When a user asks to open an app, reply with: 'Opening [App Name]'"
            )
        ]
    )

    try:
        response_stream = client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config,
        )
        response_text = "".join(chunk.text for chunk in response_stream)

        # Append model response to chat history
        chat_history.append({
            "role": "model",
            "text": response_text
        })

        # Update session
        session["chat_history"] = chat_history

        return response_text, 200, {"Content-Type": "text/plain"}

    except Exception as e:
        return f"Error occurred: {str(e)}", 500, {"Content-Type": "text/plain"}

@app.route("/reset", methods=["GET"])
def reset():
    session.pop("chat_history", None)
    return "Conversation history cleared.", 200

if __name__ == "__main__":
    app.run(debug=True)