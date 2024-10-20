# Discord MP3 to MP4 Bot

This Discord bot converts a combination of an image file (.jpg or .png) and an MP3 audio file into an MP4 video file. The bot listens for messages in a specific channel and processes attached files to create a video.

## Features

- Converts image (.jpg or .png) and MP3 files to MP4 video
- Limits audio duration to 5 minutes
- Automatically cleans up temporary files after processing
- Configurable working directory and scanned channel

## Requirements

- Python 3.7+
- discord.py library
- moviepy library
- python-dotenv library

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install discord.py moviepy python-dotenv
   ```
3. Create a `.env` file in the root directory with your Discord bot token:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```
4. Create a `conf.json` file in the root directory with the following structure:
   ```json
   {
     "working_dir": "path/to/your/working/directory",
     "scanned_channel": "channel-name-to-scan"
   }
   ```
   Replace `"path/to/your/working/directory"` with the desired temporary file storage location, and `"channel-name-to-scan"` with the name of the Discord channel where the bot should operate.

## Usage

1. Run the bot:
   ```
   python main.py
   ```
2. In Discord, go to the channel specified in `conf.json`
3. Upload an image file (.jpg or .png) and an MP3 file in the same message
4. The bot will process these files and return an MP4 video

## How it works

1. The bot listens for messages in the specified channel (set in `conf.json`)
2. When a message contains both an image and an MP3 file:
   - It downloads and saves these files temporarily in the working directory (set in `conf.json`)
   - Checks if the audio is shorter than 5 minutes
   - Creates a video using the image as a static frame and the MP3 as audio
   - Sends the resulting MP4 file back to the channel
   - Cleans up all temporary files

## Limitations

- Audio files must be shorter than 5 minutes
- Only processes one image and one MP3 file per message
- Only listens in the channel specified in `conf.json`

## Error Handling

The bot includes basic error handling:
- Prints detailed error messages to the console
- Sends a generic error message to the Discord channel if processing fails

## File Structure

- `main.py`: Contains the main bot code
- `.env`: Stores the Discord bot token (not tracked in git)
- `conf.json`: Configuration file for working directory and scanned channel
- `.gitignore`: Specifies intentionally untracked files
- `README.md`: This documentation file

## Contributing

Feel free to fork this repository and submit pull requests for any improvements or bug fixes.

## License

MIT LICENSE

## Hosting the Bot

While you can run this bot on your local machine, you might want to host it on a cloud platform to keep it running 24/7 without needing your PC to be on all the time. One option for this is Render, which offers free and paid tiers for hosting web services.

### Hosting on Render

1. Sign up for a Render account at https://render.com/

2. Create a new Web Service on Render:
   - Connect your GitHub repository to Render
   - Choose the repository and branch containing your bot code
   - Select the runtime as Python
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `python main.py`

3. Add environment variables:
   - In the Render dashboard, go to your web service settings
   - Add the `DISCORD_TOKEN` environment variable with your bot token

4. Modify your `conf.json`:
   - For the `working_dir`, use a path that Render allows writing to, such as `/tmp`
   - Example:
     ```json
     {
       "working_dir": "/tmp",
       "scanned_channel": "your-channel-name"
     }
     ```

5. Create a `requirements.txt` file in your repository root with the following content:
   ```
   discord.py
   moviepy
   python-dotenv
   ```

6. Push these changes to your GitHub repository

7. Deploy your service on Render

Now your bot will run continuously on Render's servers. Note that free tier services on Render may have limitations, such as spinning down after periods of inactivity. Check Render's documentation for more details on their free and paid offerings.

Remember to comply with Render's terms of service and usage policies when hosting your bot.
