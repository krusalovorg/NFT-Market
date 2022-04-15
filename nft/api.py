import requests
import subprocess, os
import web3
from web3 import contract, Web3
from eth_account import Account
import secrets

class NFTApi:
    def __init__(self, password):
        self.w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/296ed10aa2eb4a80b0959f7cea646878"))
        self.dir = os.path.abspath('.')
        self.pass_ = password

    def CreateNFT(self, name, owner, description, image, amount, price, category, private_key):
        print(private_key)
        req = requests.post("http://localhost:3000/api/create-nft", {
            "name": name,
            "owner": owner,
            "description": description,
            "image_link": image,
            "amount": amount,
            "price": price,
            "category": category,
            "password": self.pass_,
            "private_key": private_key
        })
        return req.json()

    def CreateMarketNFT(self, name, owner, description, image, amount, price, category):
        req = requests.post("http://localhost:3000/api/create-nft", {
            "name": name,
            "owner": owner,
            "description": description,
            "image_link": image,
            "amount": amount,
            "price": price,
            "category": category,
            "password": self.pass_,
            "private_key": self.pass_
        })
        return req.json()

    def GetNFTs(self, owner):
        return


    def uploadImageNFT(self, image_path):
        ipfs_hash = subprocess.check_output(['node',self.dir+'\\nft\\image_to_pinata.js', image_path])
        print("HASH:",ipfs_hash.decode())
        return ipfs_hash.decode().strip()

    def getDataBlock(self, hash_block):
        try:
            block = self.w3.eth.get_transaction(hash_block)
            print(block.input)
            #contract_ = web3.contract.Contract("0x0000")
            #data = contract_.decode_function_input(block.input)
            return block.input
        except web3.exceptions.BlockNotFound:
            return None

    def getBalance(self, address):
        try:
            balance = self.w3.eth.getBalance(address)
            return self.w3.fromWei(balance, 'Ether')
        except web3.exceptions.BlockNotFound:
            return None

    def getInfo(self):
        try:
            req = requests.post("http://localhost:3000/api/info", {
                "password": self.pass_,
            })
            return req.json()
        except:
            return "Loading.."

    def getPriceGas(self):
        try:
            gas = int(self.getInfo().get("gas") + "0000000000") #00000000000
            gas = self.w3.fromWei(gas, 'Ether')
            #100000000000000000
            #2100000
            print(gas)
            return gas
        except:
            return "Loading.."

    def createEthAccount(self):
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