"""Flask web server for Watson NLP emotion detection application.

This module exposes a web interface and API endpoint that accepts text input,
processes it using the emotion_detector function, and returns formatted
emotion analysis results for display in the browser UI.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/")
def index():
    """Render the main HTML user interface from index.html."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def get_emotion():
    """
    Process emotion detection requests via GET (browser) or POST (API).

    Returns a JSON object containing a formatted system response string.
    Returns an error message when the input text is missing or invalid.
    """
    if request.method == "GET":
        text = request.args.get("textToAnalyze")
    else:
        request_data = request.get_json()
        text = request_data.get("text") if request_data else None

    if not text:
        return jsonify({"emotion_response": "Invalid text! Please try again!"})

    result = emotion_detector(text)

    if result.get("dominant_emotion") is None:
        return jsonify({"emotion_response": "Invalid text! Please try again!"})

    response_str = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return jsonify({"emotion_response": response_str})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
