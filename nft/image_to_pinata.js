const process = require("process");
const fs = require('fs');
const pinataSDK = require('@pinata/sdk');

const PINATA_API_KEY = '9b0fb64a7f4626d4381b';
const PINATA_SECRET_API_KEY = 'b3b109e220885306edde3441c1b977bbbfe19871349af5435aa63475bb554d83';
const pinata = pinataSDK(PINATA_API_KEY, PINATA_SECRET_API_KEY);

var imgPath = process.argv[2]
const readableStreamForFile = fs.createReadStream(imgPath);
const options = {};

pinata.pinFileToIPFS(readableStreamForFile, options).then((result) => {
    console.log(result["IpfsHash"])
}).catch((err) => {
    console.log(err)
});