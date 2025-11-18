import requests
import json

def emotion_detector(text_to_analyze):
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {
        "Content-Type": "application/json",
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    # Required behavior: For status_code 400 → return all None values
    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

    # Normal success case
    if response.status_code == 200:
        result = json.loads(response.text)
        emotions = result['emotionPredictions'][0]['emotion']

        # Find dominant emotion
        dominant = max(emotions, key=emotions.get)

        return {
            "anger": emotions.get("anger"),
            "disgust": emotions.get("disgust"),
            "fear": emotions.get("fear"),
            "joy": emotions.get("joy"),
            "sadness": emotions.get("sadness"),
            "dominant_emotion": dominant
        }

    # Any other unexpected status codes
    return {
        "error": f"Request failed with status code {response.status_code}"
    }
