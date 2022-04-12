const express = require('express');
const router = express.Router();
const deploy = require("../scripts/deploy")
const mintNFT = require("../scripts/mint-nft")
const LoadNFT = require("../scripts/load_nft")

router.use(function timeLog(req, res, next) {
  console.log('Time: ', Date.now());
  next();
});

router.post('/create-nft', async function(req, res) {
    try {
        const {owner, name, description, image_link, amount, price} = req.body;

        console.log(req.body)

        const result = await LoadNFT(image_link, "0xd0047e035D8ba9B11f45Fa92bD4F474fa191e621");
        const status = result.status

        if (status) {
            console.log("NFT создан успешно:", result.contract)
            return res.json({"status":"true", "hash_block": result.hash_block})
        } else {
            console.log("Контракт не создан:",result)
        }

        /*const deploy_contract = await deploy()
        const adr_contract = deploy_contract.contract
        const status = deploy_contract.status

        if (true) {
            console.log("Deploy succed!")
            console.log(adr_contract, image_link, owner)
            const mint_nft = await mintNFT(adr_contract, image_link, "0xd0047e035D8ba9B11f45Fa92bD4F474fa191e621")//adr_contract
            console.log("MINT:",mint_nft)
            if (mint_nft.status) {
                console.log("Mint succed!")
                console.log("Hash:",mint_nft.contract)
                return res.json({status:"true", contract: mint_nft.contract})
            }    
        } else {
            return res.json({"status":"false", error: deploy_contract.error})
        }*/

        return res.json({"status":"false"})
    } catch (e) {
        console.log(e.message)
        console.log(e)
        res.status(500).json({ message : "Something went wrong, try again"})
    }
});

router.get('/create-nft', function(req, res) {
    try {
        return res.send("work")
    } catch (e) {
        console.log(e.message)
        console.log(e)
        res.status(500).json({ message : "Something went wrong, try again"})
    }
});

module.exports = router;