import requests


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