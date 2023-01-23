""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://linkfree.antonionardella.it)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

from discord.ext import commands
from discord.ext.commands import Context
import pickle
import json


from helpers import checks
import traceback

# Open the config.json file
with open("config.json") as file:
        config = json.load(file)

bot_reply_channel_id = "1006484431722262618"

# Here we name the cog and create a new class for the cog.
class Tokens(commands.Cog, name="tokens"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.hybrid_command(
        name="richlist-iota",
        description="Gives the Top 5 IOTA addresses",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()

    async def richlist_iota(self, context: Context):
        """
        This command prints and embed with the top 5 IOTA addresses.

        :param context: The application command context.
        """
        global bot_reply_channel_id
        # Do your stuff here

        if context.message.channel.id != int(bot_reply_channel_id):
            await context.send(f"This command can only be used in the <#{bot_reply_channel_id}> channel.")
            return

        try:
            with open('embed_iota_richlist.pkl', 'rb') as f:
                embed = pickle.load(f)
            await context.send(embed=embed)

        except Exception as e:
            print(traceback.format_exc())
    
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.hybrid_command(
        name="richlist-shimmer",
        description="Gives the Top 5 Shimmer addresses",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()

    async def richlist_shimmer(self, context: Context):
        """
        This command prints and embed with the top 5 Shimmer addresses.

        :param context: The application command context.
        """
        # Do your stuff here
        global bot_reply_channel_id
        # Do your stuff here

        if context.message.channel.id != int(bot_reply_channel_id):
            await context.send(f"This command can only be used in the <#{bot_reply_channel_id}> channel.")
            return      
        
        try:
            with open('embed_shimmer_richlist.pkl', 'rb') as f:
                embed = pickle.load(f)
            await context.send(embed=embed)

        except Exception as e:
            print(traceback.format_exc())

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Tokens(bot))
