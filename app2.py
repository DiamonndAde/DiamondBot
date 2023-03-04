import discord
import requests
import os
import json
from web3 import Web3
from web3.contract import ConciseContract

ETHERSCAN_API_KEY = 'AQE8RH6N1H4TDSST89IUXHIF8TRXUH64QZ'
# 0x839c6Ca36F51Fc2DBf466e027B8a57f840dc9C57

# Instantiate Web3 with Infura API endpoint
web3 = Web3(Web3.HTTPProvider(
    'https://mainnet.infura.io/v3/0dabef1094224089b08c07c96398c85b'))

# Read the contract ABI from a JSON file


def get_contract_abi(contract_address):
    # Set up the Etherscan API endpoint and parameters
    api_endpoint = 'https://api.etherscan.io/api'
    api_key = 'AQE8RH6N1H4TDSST89IUXHIF8TRXUH64QZ'
    module = 'contract'
    action = 'getabi'
    address = contract_address

    # Build the API request URL
    url = f'{api_endpoint}?module={module}&action={action}&address={address}&apikey={api_key}'

    # Make the API request and fetch the ABI
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data.get('result')
    else:
        print('Failed to fetch contract ABI.')
        return ''


def calculate_profit(wallet_address, collection_identifier):
    # Set up the web3 provider using Infura

    # Determine if the collection identifier is a contract address or a collection name
    if web3.isAddress(collection_identifier):
        contract_address = collection_identifier
    else:
        # Fetch the contract address associated with the collection name
        response = requests.get(
            f'https://api.opensea.io/api/v1/collection/{collection_identifier}/')
        if response.ok:
            data = response.json()
            contract_address = data.get('primary_asset_contracts')[
                0].get('address')
        else:
            print('Failed to fetch contract address.')
            return 0

    # Generate the contract ABI
    contract_abi = get_contract_abi(contract_address)
    print(contract_abi)

    # Create a contract instance
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    token_ids = contract.functions.tokensOfOwner(wallet_address).call()
    print(token_ids)

    # Calculate the profit for each token
    total_profit = 0
    for token_id in token_ids:
        print(token_id)
        response = requests.get(
            f'https://api.opensea.io/api/v1/asset/{contract_address}/{token_id}/')
        print(response)
        if response.ok:
            data = response.json()
            price = data.get('last_sale').get('total_price')
            print(price)
            total_profit += int(price) / 1000000000000000000
            print(total_profit)

    # Return the total profit
    return total_profit

    # Fetch the NFTs owned by the wallet address
    # owned_nfts = []
    # for i in range(contract.functions.balanceOf(wallet_address).call()):
    #     token_id = contract.functions.tokenOfOwnerByIndex(
    #         wallet_address, i).call()
    #     owned_nfts.append(token_id)

    # # Fetch the metadata for each NFT and calculate the total profit
    # total_profit = 0
    # for nft_id in owned_nfts:
    #     response = requests.get(
    #         f'https://api.opensea.io/api/v1/asset/{contract_address}/{nft_id}/')
    #     if response.ok:
    #         data = response.json()
    #         price = data.get('last_sale').get('total_price')
    #         total_profit += int(price) / 1000000000000000000

    # return total_profit


print(calculate_profit('0xBDcE6D8df8CB76a35aA0109C0736B10Ca5521c55',
      '0x839c6Ca36F51Fc2DBf466e027B8a57f840dc9C57'))


# wallet_addresses = ["0x9Ebd725E2767F4997dC1fA9515e1a6C545B015a9", "0xaF514772FF826159617d19AE1C284027D8118D23", "0x2d70BE92de0F137437633fb4bE55DEf4168e3609", "0xfedA665529d1E8184420C2139Fe01b66be0a3d40", "0xe27737BbF129f5C8aff953f13E65444d0B89Bbe5",
#                     "0xeDF644A6A0C1a8a6C4f3aEe0B9A85a55790a2aD7", "0x5429d0Cf4daEA3c00F2fCd340cBc22756fB0AA89", "0x1eB79804a7C385700592640753476Ae32F55f9F9", "0x1cd0B0Eb3d6D4Be2B05Cc470da788243968AE845", "0x2c6430A2882b18d30cC47e41867bE7FeC6670DF4"]

# for wallet_address in wallet_addresses:
#     print(wallet_address, get_wallet_info(wallet_address))

# Initialize the Discord client
# client = discord.Client()

# # Define a command to get wallet information


# @client.event
# async def on_message(message):
#     if message.content.startswith('!wallet '):
#         wallet_address = message.content.split(' ')[1]
#         try:
#             info = get_wallet_info(wallet_address)
#             response = '\n'.join([f'{k}: {v}' for k, v in info.items()])
#         except:
#             response = 'Error: could not fetch wallet information'
#         await message.channel.send(response)

# # Run the bot
# client.run(
#     'MTA3ODgzMzAwNTM0ODUyNDA0Mg.GDaXFY.MjKiU4pZx5m89tXKdzMiyKfcAQyByWNra2YUqY')
