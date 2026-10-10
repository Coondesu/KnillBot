import discord
from discord.ext import commands
import os

token = os.getenv("DISCORD_TOKEN")

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.moderation")
        await self.load_extension("cogs.extra")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} slash commands")


intents = discord.Intents.default()

bot = MyBot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot.run(token)