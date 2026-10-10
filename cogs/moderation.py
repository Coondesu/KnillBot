import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ban",
        description="Ban a member from the server"
    )
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(
        member="The member to ban",
        reason="Reason for the ban"
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "This command only works in a server.",
                ephemeral=True
            )
            return

        if member.id == interaction.user.id:
            await interaction.response.send_message(
                "You cannot ban yourself!",
                ephemeral=True
            )
            return

        if member.id == guild.owner_id:
            await interaction.response.send_message(
                "You cannot ban the server owner.",
                ephemeral=True
            )
            return

        bot_member = guild.me

        if not bot_member.guild_permissions.ban_members:
            await interaction.response.send_message(
                "I need the Ban Members permission.",
                ephemeral=True
            )
            return

        if member.top_role >= bot_member.top_role:
            await interaction.response.send_message(
                "That member's highest role must be below my highest role.",
                ephemeral=True
            )
            return

        try:
            await member.ban(
                reason=f"{reason} | Banned by {interaction.user}"
            )

            await interaction.response.send_message(
                f"Banned **{member}**.\nReason: {reason}",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "Discord denied the ban. Check my permissions and role hierarchy.",
                ephemeral=True
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "The ban failed due to a Discord API error.",
                ephemeral=True
            )

    @app_commands.command(
        name="kick",
        description="Kick a member from the server"
    )
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(
        member="The member to kick",
        reason="Reason for the kick"
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command only works in a server.",
                ephemeral=True
            )
            return

        if member.id == interaction.user.id:
            await interaction.response.send_message(
                "You cannot kick yourself!",
                ephemeral=True
            )
            return

        if member.id == guild.owner_id:
            await interaction.response.send_message(
                "You cannot kick the server owner.",
                ephemeral=True
            )
            return

        bot_member = guild.me

        if not bot_member.guild_permissions.kick_members:
            await interaction.response.send_message(
                "I need the Kick Members permission.",
                ephemeral=True
            )
            return

        if member.top_role >= bot_member.top_role:
            await interaction.response.send_message(
                "That member's highest role must be below my highest role.",
                ephemeral=True
            )
            return

        try:
            await member.kick(
                reason=f"{reason} | Kicked by {interaction.user}"
            )

            await interaction.response.send_message(
                f"👢 Kicked **{member}**.\nReason: {reason}",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "Discord denied the kick. Check my permissions and role hierarchy.",
                ephemeral=True
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "The kick failed due to a Discord API error.",
                ephemeral=True
            )

    @app_commands.command(
        name="mute",
        description="Timeout a member in the server"
    )
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(
        member="The member to mute",
        duration="Timeout duration in minutes (1-40320)",
        reason="Reason for the timeout"
    )
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: app_commands.Range[int, 1, 40320],
        reason: str = "No reason provided"
    ):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "This command only works in a server.",
                ephemeral=True
            )
            return

        if member.id == interaction.user.id:
            await interaction.response.send_message(
                "You cannot mute yourself!",
                ephemeral=True
            )
            return

        if member.id == guild.owner_id:
            await interaction.response.send_message(
                "You cannot mute the server owner.",
                ephemeral=True
            )
            return

        bot_member = guild.me

        if bot_member is None:
            await interaction.response.send_message(
                "I couldn't verify my server permissions.",
                ephemeral=True
            )
            return

        if not bot_member.guild_permissions.moderate_members:
            await interaction.response.send_message(
                "I need the Moderate Members permission.",
                ephemeral=True
            )
            return

        if member.top_role >= bot_member.top_role:
            await interaction.response.send_message(
                "That member's highest role must be below my highest role.",
                ephemeral=True
            )
            return

        if member.timed_out_until is not None:
            await interaction.response.send_message(
                "That member is already timed out.",
                ephemeral=True
            )
            return

        from datetime import timedelta

        try:
            await member.timeout(
                timedelta(minutes=duration),
                reason=f"{reason} | Muted by {interaction.user}"
            )

            await interaction.response.send_message(
                f"**{member}** has been muted for "
                f"**{duration} minute(s)**.\n"
                f"Reason: {reason}",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "Discord denied the timeout. Check my permissions "
                "and role hierarchy.",
                ephemeral=True
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "The mute failed due to a Discord API error.",
                ephemeral=True
            )

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))