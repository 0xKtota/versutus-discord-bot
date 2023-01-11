""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://linkfree.antonionardella.it)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
import urllib.request

# Here we name the cog and create a new class for the cog.
class ShimmerEvm(commands.Cog, name="ShimmerEVM"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="goshimmerstatus",
        description="Verify if the node is up and give the status.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    #checks.is_owner()
    async def goshimmerstatus(self, context: Context):
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        # Set goshimmer_status variable
        emvstatus = "Something is wrong, mate!"
        # Do your stuff here
        try:
            response = urllib.request.urlopen("http://node-02.feature.shimmer.iota.cafe:8081/")
            print("Response Code:", response.getcode())
            goshimmer_status = response.getcode()
            
            embed = discord.Embed(title = "✅ The node answered", color=0x00FF00)
            embed.add_field(name = "Response Code: ", value =  goshimmer_status)
            embed.add_field(name = "Monitored node: ", value = "http://node-02.feature.shimmer.iota.cafe:8081/")
            await context.send(embed=embed)
        
        except urllib.error.HTTPError as e:
            print("HTTP Error:", e.reason)
            goshimmer_status = "{}".format(e.reason)

            embed = discord.Embed(title = "❌ A HTTP error occurred", color=0xFF0000)
            embed.add_field(name = "HTTP Error: ", value =  goshimmer_status)
            embed.add_field(name = "Monitored node: ", value = "http://node-02.feature.shimmer.iota.cafe:8081/")
            await context.send(embed=embed)
        
        except urllib.error.URLError as e:
            print("URL Error:", e.reason)
            goshimmer_status = "{}".format(e.reason)
            
            embed = discord.Embed(title = "❌ An URL error occurred", color=0xFF0000)
            embed.add_field(name = "URL Error: ", value =  goshimmer_status)
            embed.add_field(name = "Monitored node: ", value = "http://node-02.feature.shimmer.iota.cafe:8081/")
            await context.send(embed=embed)
        
        except Exception as e:
            print("Other Error:", str(e))
            goshimmer_status = str(e)
            
            embed = discord.Embed(title = "❌ An other error occurred", color=0xFF0000)
            embed.add_field(name = "Other Error: ", value =  goshimmer_status)
            embed.add_field(name = "Monitored node: ", value = "http://node-02.feature.shimmer.iota.cafe:8081/")
            await context.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(ShimmerEvm(bot))
