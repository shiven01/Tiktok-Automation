# Reddit to TikTok Automation

This project automates the creation of TikTok videos using content from Reddit posts and background videos from YouTube.

## Features

- Scrapes text content from Reddit posts using PRAW
- Downloads background videos from YouTube
- Converts text to speech using ElevenLabs API
- Generates subtitles for the speech
- Combines all elements into a final video

## Prerequisites

- Python 3.7+
- FFmpeg
- eSpeak

Ensure these executables can be called from your shell:
```
espeak, ffmpeg, ffprobe, pip, python
```

## Setup

1. Clone this repository
2. Install required packages:
   ```
   pip install numpy aeneas
   pip install -r requirements.txt
   ```
3. Verify Aeneas installation:
   ```
   python -m aeneas.diagnostics
   ```
4. Copy `.env.template` to `.env` and fill in your API credentials

## Environment Variables

Set up the following environment variables in your `.env` file:

- REDDIT_CLIENT_ID
- REDDIT_CLIENT_SECRET
- REDDIT_USER_PASSWORD
- REDDIT_USER_AGENT
- REDDIT_USER_USERNAME
- XI_API_KEY (ElevenLabs API key)
- YT_MP4_RAPIDAPI_KEY (YouTube to MP4 conversion API key)

## Usage

Run the script:

```
python video-generator.py
```

Follow the prompts to enter:
1. The URL of the Reddit post
2. The URL of the YouTube video to use as background

The script will generate a video file named `reddit_post_video.mp4`.

## Future Development

- Implement TikTok API integration for automated posting
- Develop a user interface for easier operation
- Implement content filtering and customization options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024 Shiven Shekar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Disclaimer

This tool is for educational purposes only. Ensure you comply with Reddit's API terms of service, YouTube's terms of service, and TikTok's community guidelines when using this tool.
