import praw
import os
import requests

# Reddit API Setup
reddit = praw.Reddit(
        client_id = os.environ.get('REDDIT_CLIENT_ID'),
        client_secret = os.environ.get('REDDIT_CLIENT_SECRET'),
        password = os.environ.get('REDDIT_USER_PASSWORD'),
        user_agent = os.environ.get('REDDIT_USER_AGENT'),
        username = os.environ.get('REDDIT_USER_USERNAME')
        )
reddit.read_only = True

# ElevenLabs API Setup
XI_API_KEY = os.environ.get('XI_API_KEY')
print(f"API Key: {XI_API_KEY}")  # Debug print
VOICE_ID = "2EiwWnXFnvU5JabPnv8n"

def get_reddit_post_text(url):
    submission = reddit.submission(url=url)
    return f"Title: {submission.title}\n\nContent: {submission.selftext}"

def generate_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": XI_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("reddit_post_audio.mp3", "wb") as f:
            f.write(response.content)
        print("Audio generated successfully. Saved as 'reddit_post_audio.mp3'")
    else:
        print(f"Error generating speech: {response.status_code}")
        print(response.text)

# Main execution
if __name__ == "__main__":
    reddit_post_url = input("Enter the URL of the Reddit post: ")
    post_text = get_reddit_post_text(reddit_post_url)
    print("Retrieved text from Reddit post:")
    print(post_text)
    print("\nGenerating speech from this text...")
    generate_speech(post_text)
