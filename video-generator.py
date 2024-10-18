import praw
import os
import requests
import ffmpeg
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from aeneas.textfile import TextFileFormat
from aeneas.language import Language
from aeneas.logger import Logger
from urllib.parse import urlparse, parse_qs

def verify_env_variables():
    print("Checking environment variables:")
    variables = [
        'YT_MP4_RAPIDAPI_KEY',
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'REDDIT_USER_PASSWORD',
        'REDDIT_USER_AGENT',
        'REDDIT_USER_USERNAME',
        'XI_API_KEY'
    ]
    
    for var in variables:
        value = os.getenv(var)
        if value:
            print(f"  {var}: {'*' * len(value)}")
        else:
            print(f"  {var}: Not set")

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
VOICE_ID = "2EiwWnXFnvU5JabPnv8n"

# YT to MP4 API Setup
RAPIDAPI_KEY = os.environ.get('YT_MP4_RAPIDAPI_KEY')

def get_youtube_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def download_youtube_video(youtube_url):
    video_id = get_youtube_id(youtube_url)
    if not video_id:
        print("Invalid YouTube URL")
        return None

    url = f"https://ytstream-download-youtube-videos.p.rapidapi.com/dl?id={video_id}"
    headers = {
        "x-rapidapi-host": "ytstream-download-youtube-videos.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    print(f"Making request to: {url}")
    print(f"Headers: {headers}")

    try:
        response = requests.get(url, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text[:500]}...")  # Print first 500 characters

        response.raise_for_status()
        data = response.json()
        
        if 'formats' not in data or not data['formats']:
            print(f"No video formats found. API response: {data}")
            return None
        
        video_url = data['formats'][-1]['url']
        print(f"Video URL: {video_url}")

        video_response = requests.get(video_url)
        video_response.raise_for_status()
        
        with open("background.mp4", "wb") as f:
            f.write(video_response.content)
        print("YouTube video downloaded successfully as 'background.mp4'")
        return "background.mp4"
    
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        if response.status_code == 401:
            print("API key may be invalid or expired.")
        elif response.status_code == 429:
            print("Rate limit exceeded. Please wait before trying again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

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
        audio_file = "reddit_post_audio.mp3"
        with open(audio_file, "wb") as f:
            f.write(response.content)
        print(f"Audio generated successfully. Saved as '{audio_file}'")
        return audio_file
    else:
        print(f"Error generating speech: {response.status_code}")
        print(response.text)
        return None

def generate_subtitles(text, audio_file):
    print(f"Generating subtitles for audio file: {audio_file}")
    print(f"Text content: {text[:100]}...")  # Print first 100 characters of text

    # Create a temporary text file
    with open("temp_text.txt", "w") as f:
        f.write(text)
    print("Temporary text file created.")

    # Create a Task object
    config_string = "task_language=eng|is_text_type=plain|os_task_file_format=srt"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = os.path.abspath(audio_file)
    task.text_file_path_absolute = os.path.abspath("temp_text.txt")
    task.sync_map_file_path_absolute = os.path.abspath("subtitles.srt")

    print(f"Audio file path: {task.audio_file_path_absolute}")
    print(f"Text file path: {task.text_file_path_absolute}")
    print(f"Subtitle file path: {task.sync_map_file_path_absolute}")

    # Add detailed logging
    logger = Logger(tee=Logger.DEBUG)
    task.logger = logger

    try:
        ExecuteTask(task).execute()
        print("Subtitle generation task executed successfully.")
        print(f"Task output: {task.output_sync_map_file()}")
    except Exception as e:
        print(f"Error during subtitle generation: {e}")
        print(f"Task details: {task.to_string()}")

    # Clean up the temporary text file
    os.remove("temp_text.txt")
    print("Temporary text file removed.")

    # Check file permissions
    print(f"Current working directory: {os.getcwd()}")
    print(f"Permissions for current directory: {oct(os.stat('.').st_mode)[-3:]}")
    print(f"User ID: {os.getuid()}, Group ID: {os.getgid()}")

    # Verify subtitle file creation
    if os.path.exists("subtitles.srt"):
        print("Subtitle file created successfully.")
        with open("subtitles.srt", "r") as f:
            print(f"First 100 characters of subtitles: {f.read(100)}")
    else:
        print("Subtitle file was not created.")

    return "subtitles.srt"

def create_video(background_video, audio_file, subtitle_file, output_file):
    # Check if all required files exist
    for file in [background_video, audio_file, subtitle_file]:
        if not os.path.exists(file):
            print(f"Error: File {file} does not exist.")
            return

    video = ffmpeg.input(background_video)
    audio = ffmpeg.input(audio_file)
    
    # Scale the video and split the output
    scaled = ffmpeg.filter(video, 'scale', 1080, 1920)
    split = ffmpeg.filter(scaled, 'split')
    
    # Apply subtitles to one of the split outputs
    subtitled = ffmpeg.filter(split, 'subtitles', subtitle_file, force_style='Fontsize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=20')
    
    # Combine the video and audio
    output = ffmpeg.output(subtitled, audio, output_file)
    
    try:
        ffmpeg.run(output)
        print(f"Video created successfully: {output_file}")
    except ffmpeg.Error as e:
        print(f"An error occurred while creating the video: {e.stderr.decode()}")

if __name__ == "__main__":
    verify_env_variables()
    reddit_post_url = input("Enter the URL of the Reddit post: ")
    youtube_url = input("Enter the URL of the YouTube video to use as background: ")

    post_text = get_reddit_post_text(reddit_post_url)
    print("Retrieved text from Reddit post:")
    print(post_text)
    
    print("\nDownloading YouTube video...")
    background_video = download_youtube_video(youtube_url)
    if not background_video:
        print("Failed to download YouTube video. Exiting.")
        exit()

    print("\nGenerating speech from text...")
    audio_file = generate_speech(post_text)
    
    if audio_file:
        print("\nGenerating subtitles...")
        subtitle_file = generate_subtitles(post_text, audio_file)
        
        if os.path.exists(subtitle_file):
            print("\nCreating video...")
            output_file = "reddit_post_video.mp4"
            create_video(background_video, audio_file, subtitle_file, output_file)
        else:
            print("Failed to create subtitles. Cannot proceed with video creation.")
    else:
        print("Failed to generate speech. Cannot proceed with video creation.")
