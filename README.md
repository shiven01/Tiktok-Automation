# Reddit to TikTok Automation

This project automates the process of creating TikTok videos from Reddit posts. It scrapes data from Reddit, converts the text to speech, and combines it with video content for TikTok.

## Features

- Scrapes text content from Reddit posts using PRAW
- Converts text to speech using ElevenLabs API
- (Planned) Combines audio with video for TikTok content
- (Planned) Automates posting to TikTok

## Setup

1. Clone this repository
2. Install required packages: `pip install -r requirements.txt`
3. Copy `.env.template` to `.env` and fill in your API credentials (Reddit, ElevenLabs, and TikTok)
4. Run the script: `python reddit-elevenlabs-test.py`

## Environment Variables

This project uses the following environment variables:

- REDDIT_CLIENT_ID
- REDDIT_CLIENT_SECRET
- REDDIT_USER_PASSWORD
- REDDIT_USER_AGENT
- REDDIT_USER_USERNAME
- XI_API_KEY (ElevenLabs API key)

Make sure to set these in your `.env` file or in your environment before running the script.

## Usage

1. Run the script and enter a Reddit post URL when prompted
2. The script will scrape the post content and convert it to speech
3. (Planned) The script will combine the audio with video content
4. (Planned) The resulting video will be automatically posted to TikTok

## Future Development

- Implement video creation functionality
- Add TikTok API integration for automated posting
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

This tool is for educational purposes only. Ensure you comply with Reddit's API terms of service and TikTok's community guidelines when using this tool.
