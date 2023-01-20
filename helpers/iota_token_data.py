""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""
import discord
import json
import traceback
import requests
import iota_client_production
import pickle
import datetime


from helpers import db_manager
from helpers.logger import logger

with open("config.json") as file:
        config = json.load(file)

async def get_iota_ledger_state():
    try:
        logger.info("Getting IOTA ledger state")
        # Download the latest ledger state from the IOTA HORNET debug plugin
        debug_plugin_url = 'https://chrysalis.naerd.tech/api/plugins/debug/addresses/ed25519' 
        jwt_token = config["iota_hornet_jwt_token"]

        head = {'Authorization': 'Bearer {}'.format(jwt_token)}
        headers = {'content-type': 'application/json'}

        response = requests.get(url = debug_plugin_url, headers=head)
        chrysalis_reply = response.text 
        data = json.loads(chrysalis_reply)

        await db_manager.add_iota_ledger(data = data, table_name = "iota_hex_addresses")
    
    except Exception as e:
        logger.info(traceback.format_exc())      

async def get_bech32_address_format_iota(ed25519_address):
    bech32_address = iota_client_production.Client().hex_to_bech32(ed25519_address, "iota")
    logger.info(bech32_address)
    logger.info("bech32_address")
    return bech32_address


async def save_iota_rich_list():
    try:
        logger.info("Saving IOTA rich list")
        rows = await db_manager.get_iota_ledger(table_name = "iota_hex_addresses")
        sorted_addresses = sorted(rows, key=lambda x: x[1], reverse=True)
        top_addresses = sorted_addresses[:20]
        # Convert addresses to bech32 format using map function
        top_addresses = list(map(lambda x: (iota_client_production.Client().hex_to_bech32(x[0], "iota"), x[1]), top_addresses))
        await db_manager.add_iota_top_addresses(data = top_addresses, table_name = "iota_top_addresses")
    except Exception as e:
        logger.info(traceback.format_exc())  

async def prepare_iota_embed():
    logger.info("Preparing IOTA rich list embed")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    richlist_from_db = await db_manager.get_iota_top_addresses(table_name = "iota_top_addresses")
    complete_richlist = []
    for row in richlist_from_db:
        complete_richlist.append(f"{row[0]} - {row[1]}")
        try:
            # Here we create an embed with the title "IOTA Richlist"          
            embed = discord.Embed(title = "🫰 IOTA Top 5 Richlist", color=0x00FF00)
            for i in range(5):
                if i >= len(complete_richlist):
                    break
                address, balance = complete_richlist[i].split(" - ")
                if int(balance) >= 10**15:
                    balance = f"{float(balance)/10**15:.2f} Pi"
                elif int(balance) >= 10**12:
                    balance = f"{float(balance)/10**12:.2f} Ti"
                elif int(balance) >= 10**9:
                    balance = f"{float(balance)/10**9:.2f} Gi"
                elif int(balance) >= 10**6:
                    balance = f"{float(balance)/10**6:.2f} Mi"
                elif int(balance) >= 10**3:
                    balance = f"{float(balance)/10**3:.2f} ki"
                else:
                    balance = f"{balance} i"
                embed.add_field(name=f"Top Address {i+1}", value=address)
                embed.add_field(name=f"Balance", value=balance)
                embed.add_field(name='', value='', inline=False)
            embed.add_field(name = "Updates: ", value = "Every 24h")
            embed.add_field(name = "Last Update: ", value = current_time)
            with open('embed_iota_richlist.pkl', 'wb') as f:
                pickle.dump(embed, f)
        except Exception as e:
            logger.info(traceback.format_exc())

    logger.info("IOTA richlist embed created")

async def main():
    await get_iota_ledger_state()
    await save_iota_rich_list()
    await prepare_iota_embed()


if __name__ == "__main__":
    main()