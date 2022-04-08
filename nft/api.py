import requests
from web3 import Web3, HTTPProvider

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
    print(req.json())

    return req.json()


def GetNFTs(owner):
    w3 = Web3(Web3.HTTPProvider("https://eth-rinkeby.alchemyapi.io/v2/iSm7xkVtMVgP85UJEvYOunFRFFmF9xdg"))
    return