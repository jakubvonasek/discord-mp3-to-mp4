import discord
import os
from moviepy.editor import *
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Set the working directory where files will be stored temporarily
working_dir = json.load(open('conf.json'))['working_dir']
scanned_channel = json.load(open('conf.json'))['scanned_channel']
# Ensure the working directory exists
os.makedirs(working_dir, exist_ok=True)

class Client(discord.Client):
    async def on_ready(self):
        print(f'{self.user} is now running!')

    async def on_message(self, message):
        # Ignore messages from the bot itself to avoid loops
        if message.author == self.user:
            return

        # Check if the message is from the "bot-talk" channel
        if message.channel.name == scanned_channel:
            image_file = None
            mp3_file = None

            # Loop through the attachments to find .jpg, .png, and .mp3 files
            for attachment in message.attachments:
                if attachment.filename.endswith(('.jpg', '.png')):  # Support both .jpg and .png
                    image_file = attachment
                elif attachment.filename.endswith('.mp3'):
                    mp3_file = attachment

            # If both an image and mp3 file are found, process them
            if image_file and mp3_file:
                try:
                    # Save the files locally
                    image_path = os.path.join(working_dir, image_file.filename)
                    mp3_path = os.path.join(working_dir, mp3_file.filename)
                    output_path = os.path.join(working_dir, f"{message.author.id}.mp4")

                    await image_file.save(image_path)
                    await mp3_file.save(mp3_path)

                    # Use moviepy to check the duration of the audio file
                    audio_clip = AudioFileClip(mp3_path)
                    
                    # Check if the audio is longer than 5 minutes (300 seconds)
                    if audio_clip.duration > 300:
                        await message.channel.send("The audio file is too long. Please upload an audio file shorter than 5 minutes.")
                        audio_clip.close()  # Close the audio clip before returning
                        return

                    # Create video with the image and the audio
                    image_clip = ImageClip(image_path).set_duration(audio_clip.duration)
                    video = image_clip.set_audio(audio_clip)

                    # Save the resulting video file with AAC as the audio codec
                    video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30)

                    # Send the created video back to the channel
                    await message.channel.send(file=discord.File(output_path))

                except Exception as e:
                    # If there's any error, print it
                    print(f"Error occurred: {e}")
                    await message.channel.send("An error occurred while processing the video.")

                finally:
                    # Close the clips to free up the resources
                    if audio_clip:
                        audio_clip.close()
                    if image_clip:
                        image_clip.close()

                    # Cleanup: Remove the saved files
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    if os.path.exists(mp3_path):
                        os.remove(mp3_path)
                    if os.path.exists(output_path):
                        os.remove(output_path)

# Set up the intents to read message content
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot client with the specified intents
client = Client(intents=intents)

# Run the bot using the token from your environment variables
client.run(os.getenv('DISCORD_TOKEN'))
