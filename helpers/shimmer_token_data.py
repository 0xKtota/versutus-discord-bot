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
from iota_client import IotaClient
import pickle
import datetime
import time

from helpers import db_manager
from helpers.logger import logger

with open("config.json") as file:
        config = json.load(file)

# Create an IotaClient instance
client = IotaClient({'nodes': ['https://shimmer.naerd.tech']})

# Get the node info
async def get_node_info():
    node_info = client.get_info()
    logger.info(f'{node_info}')

async def get_shimmer_ledger_state():
    # https://shimmer.naerd.tech/api/indexer/v2/blocks/0x64031faf6284682cb8badb62f7a1946fdf1be0656945dd255030d8246e5f2d5c/metadata
    try:
        logger.info("Getting Shimmer ledger state")
        api_route = 'https://shimmer.naerd.tech/api/indexer/v1/outputs/basic'
        # param_list = ['hasNativeTokens=true', 'validated=true', 'pageSize=1']
        param_list = ['validated=true', 'pageSize=1000']
        api_parameters = f'{api_route}?{"&".join(param_list)}'
        jwt_token = config["shimmer_hornet_jwt_token"]
        
        head = {'Authorization': 'Bearer {}'.format(jwt_token)}
        headers = {'content-type': 'application/json'}

        ledger_state = {}
        cursor = None   
        last_cursor = None
        while True:
            if cursor:
                api_parameters = api_parameters.split("&cursor=")[0] + f'&cursor={cursor}'
            
            try:
                response = requests.get(url=api_parameters, headers=head)
                data = response.json()
                output_ids = data['items']
            
                try:
                    # Get the outputs by their id
                    outputs = client.get_outputs(output_ids)
                    if outputs == "{'type': 'healthyNodePoolEmpty'}":
                        logger.debug("healthyNodePoolEmpty")
                        time.sleep(15)
                        continue
                    try:
                        for output_response in outputs:
                            try:
                                output = output_response['output']
                                try:
                                    pubKeyHash = output['unlockConditions'][0]['address']['pubKeyHash']
                                    value = int(output['amount'])
                                    address = pubKeyHash
                                    if address in ledger_state:
                                        ledger_state[address] += value
                                    else:
                                        ledger_state[address] = value
                                except KeyError:
                                    logger.debug("KeyError pubKeyHash not found")
                                    # 'pubKeyHash' key not present in output, skipping
                                    continue
                            except TypeError:
                                if output_response == {'type': 'healthyNodePoolEmpty'}:
                                    time.sleep(15)
                                    continue
                                else:
                                    # 'output error', skipping
                                    logger.debug("TypeError output error")
                                    raise Exception("Unexpected output_response")

                        if "cursor" in data:
                            cursor = data["cursor"]
                        else:
                            break

                        if cursor == last_cursor:
                            break
                        last_cursor = cursor
            
                    except Exception as e:
                        logger.info(traceback.format_exc()) 
                    
                    await db_manager.add_shimmer_ledger(data = ledger_state, table_name = "shimmer_hex_addresses")
                    time.sleep(3)

                except Exception as e:
                    logger.info(traceback.format_exc())


            except Exception as e:
                logger.info(traceback.format_exc())
            
    except Exception as e:
        logger.info(traceback.format_exc())
  

async def get_bech32_address_format_iota(ed25519_address):
    bech32_address = client.hex_to_bech32(ed25519_address, "smr")
    logger.info(bech32_address)
    logger.info("bech32_address")
    return bech32_address


async def save_shimmer_rich_list():
    try:
        logger.info("Saving Shimmer rich list to database")
        rows = await db_manager.get_shimmer_ledger(table_name = "shimmer_hex_addresses")
        sorted_addresses = sorted(rows, key=lambda x: x[1], reverse=True)
        top_addresses = sorted_addresses[:20]
        # Convert addresses to bech32 format using map function
        top_addresses = list(map(lambda x: (client.hex_to_bech32(x[0], "smr"), x[1]), top_addresses))
        await db_manager.add_shimmer_top_addresses(data = top_addresses, table_name = "shimmer_top_addresses")
    except Exception as e:
        logger.info(traceback.format_exc())  

async def prepare_shimmer_embed():
    logger.info("Preparing Shimmer rich list embed")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    richlist_from_db = await db_manager.get_shimmer_top_addresses(table_name = "shimmer_top_addresses")
    complete_richlist = []
    for row in richlist_from_db:
        complete_richlist.append(f"{row[0]} - {row[1]}")
        try:
            # Here we create an embed with the title "Shimmer Richlist"          
            embed = discord.Embed(title = "🫰 Shimmer Top 5 Richlist", color=0x00FF00)
            for i in range(5):
                if i >= len(complete_richlist):
                    break
                address, balance = complete_richlist[i].split(" - ")
                if int(balance) >= 10**6:
                    balance = f"{float(balance)/10**6:.2f} SMR"
                else:
                    balance = f"{float(balance):.2f} Glow"
                embed.add_field(name=f"Top Address {i+1}", value=address)
                embed.add_field(name=f"Balance", value=balance)
                embed.add_field(name='', value='', inline=False)

            embed.add_field(name = "Updates: ", value = "Every 24h")
            embed.add_field(name = "Last Update: ", value = current_time)
            with open('embed_shimmer_richlist.pkl', 'wb') as f:
                pickle.dump(embed, f)

        except Exception as e:
            logger.info(traceback.format_exc())

    logger.info("Shimmer richlist embed created")

async def main():
    await get_shimmer_ledger_state()
    await save_shimmer_rich_list()
    await prepare_shimmer_embed()


if __name__ == "__main__":
    main()
