import discord
import requests
import os
from dotenv import load_dotenv
import json
from web3 import Web3
from web3.contract import ConciseContract

load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

# Instantiate Web3 with Infura API endpoint
web3 = Web3(Web3.HTTPProvider(
    f"https://mainnet.infura.io/v3/{os.getenv('INFURA_API_KEY')}"))

# Read the contract ABI from a JSON file
with open('contract_abi.json') as f:
    contract_abi_json = f.read()


ABI = json.loads(contract_abi_json)

# Replace with the actual contract address and ABI
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

# Instantiate the contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)


def get_balance(wallet_address):
    """
    Returns the balance of the given wallet address
    """
    balance = contract.functions.balanceOf(wallet_address).call()
    return balance


def get_total_supply():
    """
    Returns the total supply of tokens
    """
    total_supply = contract.functions.totalSupply().call()
    return total_supply


def get_tokens_minted():
    """
    Returns the number of tokens that have been minted
    """
    total_supply = get_total_supply()
    tokens_minted = total_supply - get_balance(CONTRACT_ADDRESS)
    return tokens_minted


def get_tokens_bought(wallet_address):
    """
    Returns the number of tokens bought by the given wallet address
    """
    tokens_bought = contract.functions.balanceOf(wallet_address).call()
    return tokens_bought


def get_approval_cost(wallet_address):
    """
    Returns the total cost of approving the contract to spend the user's tokens
    """
    approved_tokens = contract.functions.allowance(
        wallet_address, CONTRACT_ADDRESS).call()
    approval_cost = approved_tokens * 10**-18  # Convert from wei to ETH
    return approval_cost


def get_tokens_acquired(wallet_address):
    """
    Returns the total number of tokens acquired by the given wallet address
    """
    tokens_minted = get_tokens_minted()
    tokens_bought = get_tokens_bought(wallet_address)
    tokens_acquired = tokens_minted + tokens_bought
    return tokens_acquired


def get_tokens_sold(wallet_address):
    """
    Returns the total number of tokens sold by the given wallet address
    """
    tokens_sold = contract.functions.tokensSold(wallet_address).call()
    return tokens_sold


def get_total_fees():
    """
    Returns the total fees collected by the contract
    """
    total_fees = contract.functions.totalFees().call()
    return total_fees


def get_total_mint_cost():
    """
    Returns the total cost of minting all tokens
    """
    total_mint_cost = contract.functions.totalMintCost().call()
    return total_mint_cost


def get_total_secondary_cost():
    """
    Returns the total cost of buying all tokens on the secondary market
    """
    total_secondary_cost = contract.functions.totalSecondaryCost().call()
    return total_secondary_cost


def get_transfer_costs(wallet_address):
    """
    Returns the total cost of transferring tokens from the given wallet address
    """
    transfer_costs = contract.functions.transferCosts(wallet_address).call()
    return transfer_costs


def get_total_cost(wallet_address):
    """
    Returns the total cost of acquiring tokens by the given wallet address
    """
    approval_cost = get_approval_cost(wallet_address)
    transfer_costs = get_transfer_costs(wallet_address)
    total_cost = approval_cost + transfer_costs
    return total_cost


def get_revenue(wallet_address):
    """
    Returns the total revenue generated by the given wallet address from selling tokens
    """
    tokens_sold = get_tokens_sold(wallet_address)
    revenue = tokens_sold * 10**-18  # Convert from wei to ETH
    return revenue


def get_realized_profit(wallet_address):
    """
    Returns the realized profit of the given wallet address from selling tokens
    """
    tokens_sold = get_tokens_sold(wallet_address)
    total_cost = get_total_cost(wallet_address)
    revenue = get_revenue(wallet_address)
    realized_profit = revenue - total_cost
    return realized_profit


def get_average_mint_cost():
    """
    Returns the average cost of minting a token
    """
    total_mint_cost = get_total_mint_cost()
    tokens_minted = get_tokens_minted()
    average_mint_cost = total_mint_cost / tokens_minted
    return average_mint_cost


def get_average_secondary_cost():
    """
    Returns the average cost of buying a token on the secondary market
    """
    total_secondary_cost = get_total_secondary_cost()
    tokens_bought = get_total_supply() - get_tokens_minted()
    average_secondary_cost = total_secondary_cost / tokens_bought
    return average_secondary_cost


def get_failed_mint_cost(wallet_address):
    """
    Returns the total cost of failed mint transactions for the given wallet address
    """
    failed_mint_cost = contract.functions.failedMintCost(wallet_address).call()
    return failed_mint_cost


def get_failed_mint_count(wallet_address):
    """
    Returns the number of failed mint transactions for the given wallet address
    """
    failed_mint_count = contract.functions.failedMintCount(
        wallet_address).call()
    return failed_mint_count


def get_average_total_cost(wallet_address):
    """
    Returns the average total cost of acquiring tokens by the given wallet address
    """
    total_cost = get_total_cost(wallet_address)
    tokens_acquired = get_tokens_acquired(wallet_address)
    average_total_cost = total_cost / tokens_acquired
    return average_total_cost


def get_average_sale_price(wallet_address):
    """
    Returns the average sale price of tokens sold by the given wallet address
    """
    tokens_sold = get_tokens_sold(wallet_address)
    revenue = get_revenue(wallet_address)
    average_sale_price = revenue / tokens_sold
    return average_sale_price


def get_realized_roi(wallet_address):
    """
    Returns the realized return on investment (ROI) of the given wallet address from selling tokens
    """
    realized_profit = get_realized_profit(wallet_address)
    total_cost = get_total_cost(wallet_address)
    realized_roi = realized_profit / total_cost
    return realized_roi


def get_wallet_info(wallet_address):
    tokens_minted = get_tokens_minted()
    tokens_bought = get_tokens_bought(wallet_address)
    # approval_cost = get_approval_cost(wallet_address)
    # tokens_acquired = get_tokens_acquired(wallet_address)
    # tokens_sold = get_tokens_sold(wallet_address)
    # total_fees = get_total_fees()
    # total_mint_cost = get_total_mint_cost()
    # total_secondary_cost = get_total_secondary_cost()
    # transfer_costs = get_transfer_costs(wallet_address)
    # total_cost = get_total_cost(wallet_address)
    # revenue = get_revenue(wallet_address)
    # realized_profit = get_realized_profit(wallet_address)
    # average_mint_cost = get_average_mint_cost()
    # average_secondary_cost = get_average_secondary_cost()
    # failed_mint_costs = get_failed_mint_cost(wallet_address)
    # num_failed_mints = get_failed_mint_count(wallet_address)
    # average_total_cost = get_average_total_cost(wallet_address)
    # average_sale_price = get_average_sale_price(wallet_address)
    # realized_roi = get_realized_roi(wallet_address)
    # Return the wallet information as a dictionary
    return {
        'tokens_minted': tokens_minted,
        'tokens_bought': tokens_bought,
        # 'approval_costs': approval_cost,
        # 'tokens_acquired': tokens_acquired,
        # 'tokens_sold': tokens_sold,
        # 'total_fees': total_fees,
        # 'total_mint_cost': total_mint_cost,
        # 'total_secondary_cost': total_secondary_cost,
        # 'transfer_costs': transfer_costs,
        # 'total_cost': total_cost,
        # 'revenue': revenue,
        # 'realized_profit': realized_profit,
        # 'average_mint_cost': average_mint_cost,
        # 'average_secondary_cost': average_secondary_cost,
        # 'failed_mint_costs': failed_mint_costs,
        # 'average_total_cost': average_total_cost,
        # 'average_sale_price': average_sale_price,
        # 'realized_roi': realized_roi,
        # 'num_failed_mints': num_failed_mints
    }


# print(get_wallet_info('0xBDcE6D8df8CB76a35aA0109C0736B10Ca5521c55'))


wallet_addresses = ["0x9Ebd725E2767F4997dC1fA9515e1a6C545B015a9", "0xaF514772FF826159617d19AE1C284027D8118D23", "0x2d70BE92de0F137437633fb4bE55DEf4168e3609", "0xfedA665529d1E8184420C2139Fe01b66be0a3d40", "0xe27737BbF129f5C8aff953f13E65444d0B89Bbe5",
                    "0xeDF644A6A0C1a8a6C4f3aEe0B9A85a55790a2aD7", "0x5429d0Cf4daEA3c00F2fCd340cBc22756fB0AA89", "0x1eB79804a7C385700592640753476Ae32F55f9F9", "0x1cd0B0Eb3d6D4Be2B05Cc470da788243968AE845", "0x2c6430A2882b18d30cC47e41867bE7FeC6670DF4"]

for wallet_address in wallet_addresses:
    print(wallet_address, get_wallet_info(wallet_address))

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
# client.run(os.getenv('DISCORD_TOKEN')
