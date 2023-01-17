""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://linkfree.antonionardella.it)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager
import traceback

# Here we name the cog and create a new class for the cog.
class Tokens(commands.Cog, name="tokens"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="richlist-iota",
        description="Gives the Top 20 IOTA addresses",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()

    async def richlist_iota(self, context: Context):
        """
        This command prints and embed with the top 20 IOTA addresses.

        :param context: The application command context.
        """
        # Do your stuff here
        richlist_from_db = db_manager.get_iota_top_addresses(table_name = "top_addresses")
        complete_richlist = []
        for row in richlist_from_db:
            complete_richlist.append(f"{row[0]} - {row[1]}")
        try:
            # Here we create an embed with the title "IOTA Richlist"          
            embed = discord.Embed(title = "🫰 IOTA Richlist", color=0x00FF00)
            for i, address in enumerate(complete_richlist):
              embed.add_field(name=f"Address {i+1}", value=address, inline=False)
            embed.add_field(name = "Updates: ", value = "Every 24h.", inline = False)
            await context.send(embed=embed)
        
        except Exception as e:
            print(traceback.format_exc())


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Tokens(bot))
