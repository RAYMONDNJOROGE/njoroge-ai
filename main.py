from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Replace with your actual API key
client = genai.Client(api_key="AIzaSyAPVZ4hCgLn4dxmqhTvPoMF10A1ASh0DpU")
model = "gemini-2.5-flash"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("prompt", "")

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)],
        ),
    ]

    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        response_mime_type="text/plain",
    )

    try:
        response = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config,
        ):
            response += chunk.text
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)