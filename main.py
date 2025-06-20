from flask import Flask, render_template, request
from google import genai
from google.genai import types

app = Flask(__name__)

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

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)],
        )
    ]

    config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        system_instruction=[
            types.Part.from_text(
                text="I am Njoroge A.I., a helpful assistant that helps you in your learning. "
                     "When asked your name, always respond with: 'Hello, I am Njoroge A.I., a helpful assistant that helps you in your A.I needs."
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
        return response_text, 200, {"Content-Type": "text/plain"}

    except Exception as e:
        return f"Error occurred: {str(e)}", 500, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(debug=True)