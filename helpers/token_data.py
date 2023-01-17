""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""
import json
import traceback
import requests
import db_manager
import iota_client

from helpers import db_manager

with open("../config.json") as file:
        config = json.load(file)

async def get_iota_ledger_state():
    try:
        # Download the latest ledger state from the IOTA HORNET debug plugin
        debug_plugin_url = 'https://chrysalis.naerd.tech/api/plugins/debug/addresses/ed25519' 
        print(debug_plugin_url)
        jwt_token = config["iota_hornet_jwt_token"]

        head = {'Authorization': 'Bearer {}'.format(jwt_token)}
        headers = {'content-type': 'application/json'}

        response = requests.get(url = debug_plugin_url, headers=head)
        chrysalis_reply = response.text 
        data = json.loads(chrysalis_reply)

        db_manager.add_iota_ledger(data = data, table_name = "hex_addresses")
    
    except Exception as e:
        print(traceback.format_exc())      

async def get_bech32_address_format_iota(ed25519_address):
    bech32_address = iota_client.Client().hex_to_bech32(ed25519_address, "iota")
    return bech32_address


async def save_rich_list():
    try:
        rows = db_manager.get_iota_ledger(table_name = "hex_addresses")
        sorted_addresses = sorted(rows, key=lambda x: x[1], reverse=True)
        top_addresses = sorted_addresses[:10]
        # Convert addresses to bech32 format using map function
        top_addresses = list(map(lambda x: (get_bech32_address_format_iota(x[0]), x[1]), top_addresses))
        
        db_manager.add_iota_top_addresses(data = top_addresses, table_name = "top_addresses")
    except Exception as e:
        print(traceback.format_exc())  

def main():
    get_iota_ledger_state()
    save_rich_list()


if __name__ == "__main__":
    main()