const express = require('express');
const router = express.Router();
const deploy = require("../scripts/deploy")
const mintNFT = require("../scripts/mint-nft")

router.use(function timeLog(req, res, next) {
  console.log('Time: ', Date.now());
  next();
});

router.post('/create-nft', async function(req, res) {
    try {
        const {owner, name, description, image_link, amount, price} = req.body;

        console.log(req.body)

        const deploy_contract = await deploy()
        const adr_contract = deploy_contract.contract
        const status = deploy_contract.status

        if (status) {
            console.log("Deploy succed!")
            const mint_nft = await mintNFT("0xA17e371C7A4Ef85a8197aF450041484141ea6731", image_link, owner)//adr_contract
            console.log("MINT:",mint_nft)
            if (mint_nft.status) {
                console.log("Mint succed!")
                console.log("Hash:",mint_nft.contract)
                return res.json({status:"true", contract: mint_nft.contract})
            }
        }

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