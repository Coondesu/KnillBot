import discord
from discord import app_commands
from discord.ext import commands
from .information import KNILL_KNOWLEDGE
from pathlib import Path

MUSIC_FILE = Path(__file__).parent / "riever.mp3"
FFMPEG_PATH = "ffmpeg"

import random

class Extra(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
    name="join",
    description="I shall give you company."
    )
    @app_commands.guild_only()
    async def join(self, interaction: discord.Interaction):
        member = interaction.user

        if not isinstance(member, discord.Member) or not member.voice:
            await interaction.response.send_message(
                "Join a voice channel first!",
                ephemeral=True
            )
            return

        voice = interaction.guild.voice_client
        channel = member.voice.channel

        if voice is not None and voice.is_connected():
            if voice.channel == channel:
                await interaction.response.send_message(
                    "I'm already here with you!",
                    ephemeral=True
                )
            else:
                await voice.move_to(channel)
                await interaction.response.send_message(
                    "Joined your voice channel!"
                )
            return

        await interaction.response.defer()

        try:
            await channel.connect()
            await interaction.followup.send(
                "Joined your voice channel! 🎵"
            )
        except Exception as e:
            await interaction.followup.send(
                f"Couldn't join: {type(e).__name__}: {e}",
                ephemeral=True
            )

    @app_commands.command(
    name="leave",
    description="Need time to think?"
    )
    @app_commands.guild_only()
    async def leave(self, interaction: discord.Interaction):
        voice = interaction.guild.voice_client

        if voice is None or not voice.is_connected():
            await interaction.response.send_message(
                "I'm not in a voice channel!",
                ephemeral=True
            )
            return

        await voice.disconnect()

        await interaction.response.send_message(
            "Until next time."
        )

    @app_commands.command(
    name="music",
    description="Play the Music"
    )
    @app_commands.guild_only()
    async def music(self, interaction: discord.Interaction):
        member = interaction.user

        if not isinstance(member, discord.Member) or not member.voice:
            await interaction.response.send_message(
                "Join a voice channel first!",
                ephemeral=True
            )
            return

        if not MUSIC_FILE.is_file():
            await interaction.response.send_message(
                f"MP3 not found: {MUSIC_FILE}",
                ephemeral=True
            )
            return

        voice = interaction.guild.voice_client
        channel = member.voice.channel

        await interaction.response.defer()

        try:
            if voice is None or not voice.is_connected():
                voice = await channel.connect()
            elif voice.channel != channel:
                await interaction.followup.send(
                    "I'm already in another voice channel!",
                    ephemeral=True
                )
                return
            if voice.is_playing() or voice.is_paused():
                voice.stop()

            source = discord.FFmpegPCMAudio(
                str(MUSIC_FILE),
                executable=FFMPEG_PATH,
                before_options="-stream_loop -1"
            )

            voice.play(source)

            await interaction.followup.send("🎵 Playing music!")

        except Exception as e:
            await interaction.followup.send(
                f"Failed to play music: `{type(e).__name__}: {e}`",
                ephemeral=True
            )

    @app_commands.command(
        name="stop",
        description="Stop the music"
    )
    @app_commands.guild_only()
    async def stop(self, interaction: discord.Interaction):
        voice = interaction.guild.voice_client

        if voice is None or not voice.is_connected():
            await interaction.response.send_message(
                "I'm not in a voice channel!",
                ephemeral=True
            )
            return

        if not voice.is_playing() and not voice.is_paused():
            await interaction.response.send_message(
                "I'm connected, but nothing is playing.",
                ephemeral=True
            )
            return

        voice.stop()

        await interaction.response.send_message(
            "Theme stopped."
        )

    @app_commands.command(
    name="greet",
    description="Knill shall greet you."
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=True,
        private_channels=True
    )
    async def greet(self, interaction: discord.Interaction):
        greetings = [
            "Good day, Sir Riever.",
            "How may I assist you today, Sir Riever?",
            "It is a momentaneously mysterious day, Sir Riever.",
            "Greetings, Sir Riever.",
            "A fine day to you, Sir Riever.",
        ]

        await interaction.response.send_message(
            random.choice(greetings)
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Extra(bot))