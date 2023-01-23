import asyncio
import numpy
import pandas as pd

from helpers import db_manager

async def create_token_disribution():
    ledger_state = await db_manager.get_iota_ledger(table_name = "iota_hex_addresses")
    # Define the ranges for each bracket
    ranges = [(0, 1000000), (1000000, 10000000), (10000000, 100000000), (100000000, 1000000000), (1000000000, 10000000000), (10000000000, 100000000000), (100000000000, 1000000000000), (1000000000000, 10000000000000), (10000000000000, 100000000000000)]
    labels = ['1 Mi - 10 Mi', '10 Mi - 100 Mi', '100 Mi - 1 Gi', '1 Gi - 10 Gi', '10 Gi - 100 Gi', '100 Gi - 1 Ti', '1 Ti - 10 Ti', '10 Ti - 100 Ti', '100 Ti - 1 Pi']
    # Create a dataframe from ledger_state
    ledger_df = pd.DataFrame(ledger_state, columns=["address", "balance"])
    bin_edges = numpy.linspace(start=ranges[0][0], stop=ranges[-1][1], num=len(ranges)+1)
    ledger_df['range'] = pd.cut(ledger_df['balance'], bins=bin_edges, labels=labels)
    # Create a summary table using the 'range' column as the first column
    summary_table = ledger_df.groupby(by='range').agg({'address': 'count', 'balance': 'sum'}).reset_index()
    summary_table.rename(columns={'address':'Addresses', 'balance':'Sum balances'}, inplace=True)
    summary_table.rename(columns={'1':'Count'}, inplace=True)
    summary_table['Addresses'] = summary_table['count']
    summary_table['% Addresses'] = summary_table['count'] / summary_table['count'].sum() * 100
    summary_table['Sum balances'] = summary_table['Count'] / 1000000
    summary_table['% Supply'] = summary_table['Sum balances'].cumsum() / summary_table['Sum balances'].sum() * 100

    # Print the summary table
    print(summary_table)

async def main():
    await create_token_disribution()

asyncio.run(main())
