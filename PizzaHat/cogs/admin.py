import discord
from core.bot import PizzaHat
from core.cog import Cog
from discord.ext import commands
from discord.ext.commands import Context
from utils.custom_checks import server_staff_role

from .tickets import TicketView


class Admin(Cog, emoji=916988537264570368):
    """Admin configuration commands."""

    def __init__(self, bot: PizzaHat):
        self.bot: PizzaHat = bot

    @commands.group(invoke_without_command=True, aliases=["setup"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    async def set(self, ctx: Context):
        """
        Use this command to set something up.

        In order for this to work, the bot must have Manage Server permissions.

        To use this command, you must have Manage Server permission.
        """

        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)

    @set.command(aliases=["modrole"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def staffrole(self, ctx: Context, role: discord.Role):
        """
        Set a staff/mod-role.
        To replace the role, simply run this command again.

        In order for this to work, the bot must have Manage Server permissions.

        To use this command, you must have Manage Server permission.
        """

        try:
            if self.bot.db and ctx.guild is not None:
                await self.bot.db.execute(
                    "INSERT INTO staff_role (guild_id, role_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET role_id=$2",
                    ctx.guild.id,
                    role.id,
                )
                await ctx.send(f"{self.bot.yes} Staff role set to {role.name}")

        except Exception as e:
            await ctx.send(f"{self.bot.no} Something went wrong...")
            print(f"Error in set staffrole cmd: {e}")

    @set.command(aliases=["log"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def logs(self, ctx: Context, channel: discord.TextChannel):
        """
        Set a mod-log channel.
        To replace a log channel, simply run this command again.

        In order for this to work, the bot must have Manage Server permissions.

        To use this command, you must have Manage Server permission.
        """

        try:
            if self.bot.db and ctx.guild is not None:
                await self.bot.db.execute(
                    "INSERT INTO modlogs (guild_id, channel_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET channel_id=$2",
                    ctx.guild.id,
                    channel.id,
                )
                await ctx.send(f"{self.bot.yes} Mod-logs channel set to {channel}")

        except Exception as e:
            await ctx.send(f"{self.bot.no} Something went wrong...")
            print(f"Error in set logs cmd: {e}")

    @server_staff_role()
    @set.command(aliases=["ticket"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def tickets(self, ctx: Context, channel: discord.TextChannel):
        """
        Set up the Tickets system in the server by sending the `Create Ticket` message.

        In order for this to work, the bot must have Manage Server permissions.

        To use this command, you must have Manage Server permission.
        """

        em = discord.Embed(
            title="Create a ticket!",
            description="Click <:ticket_emoji:1004648922158989404> to create/open a new ticket.",
            color=discord.Color.gold(),
        )
        em.set_thumbnail(url="https://i.imgur.com/mOTlTBy.png")

        view = TicketView(self.bot)
        await channel.send(embed=em, view=view)
        await ctx.message.add_reaction(self.bot.yes)


async def setup(bot):
    await bot.add_cog(Admin(bot))
