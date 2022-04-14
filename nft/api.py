import requests
import subprocess, os
import web3
from web3 import contract, Web3
from eth_account import Account
import secrets


def CreateNFT(name, owner, description, image, amount, price, category):
    req = requests.post("http://localhost:3000/api/create-nft", {
        "name": name,
        "owner": owner,
        "description": description,
        "image_link": image,
        "amount": amount,
        "price": price,
        "category": category
    })
    return req.json()


def GetNFTs(owner):
    w3 = Web3(Web3.HTTPProvider("https://eth-rinkeby.alchemyapi.io/v2/iSm7xkVtMVgP85UJEvYOunFRFFmF9xdg"))
    return

dir = os.path.abspath('.')

def uploadImageNFT(image_path):
    api_key = "9b0fb64a7f4626d4381b"
    api_secret = "b3b109e220885306edde3441c1b977bbbfe19871349af5435aa63475bb554d83"
    jwt_token = "eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI3MzhmMTZjZi1kNGMyLTQxMmYtYTgyZC00MzNkYjc0YmE5YTEiLCJlbWFpbCI6ImtydXNhbG92cHJvQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2V9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI5YjBmYjY0YTdmNDYyNmQ0MzgxYiIsInNjb3BlZEtleVNlY3JldCI6ImIzYjEwOWUyMjA4ODUzMDZlZGRlMzQ0MWMxYjk3N2JiYmZlMTk4NzEzNDlhZjU0MzVhYTYzNDc1YmI1NTRkODMiLCJpYXQiOjE2NDk2OTIxNjV9.8jRdBvvlKJEzWzokvmBzvXO1LcJyWdSvY2bA_JjZd0M"
    ipfs_hash = subprocess.check_output(['node',dir+'\\nft\\image_to_pinata.js', image_path])
    print("HASH:",ipfs_hash.decode())
    return ipfs_hash.decode().strip()

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/296ed10aa2eb4a80b0959f7cea646878"))

def getDataBlock(hash_block):
    try:
        block = w3.eth.get_transaction(hash_block)
        print(block.input)
        #contract_ = web3.contract.Contract("0x0000")
        #data = contract_.decode_function_input(block.input)
        return block.input
    except web3.exceptions.BlockNotFound:
        return None

def createEthAccount():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address

# def addMetadata(name, owner, description, image, amount, price, category, block_hash):
#     db.insert({
#         "name": name,
#         "owner": owner,
#         "description": description,
#         "image_link": image,
#         "amount": amount,
#         "price": price,
#         "category": category,
#         "hash": block_hash
#     })
#     return True
#
# def getMetadata(block_hash):
#     return db.search(Metadata.hash == block_hash)