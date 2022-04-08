require("dotenv").config();

const hre = require("hardhat");

const ethers = hre.ethers

const API_URL = process.env.API_URL;

const { createAlchemyWeb3 } = require("@alch/alchemy-web3");

const alchemyWeb3 = createAlchemyWeb3(API_URL);
const contract = require("../artifacts/contracts/OsunRiverNFT.sol/MarketNFT.json");
const METAMASK_PUBLIC_KEY = process.env.METAMASK_PUBLIC_KEY;
const METAMASK_PRIVATE_KEY = process.env.METAMASK_PRIVATE_KEY;
//const contractAddress = "0x68512832bDD76E93c421Ae2F2bBDeC9aF401bB44";

module.exports = async function mintNFT(contractAddress, tokenURI, newOwner) {
  // get the nonce - nonce is needed for security reasons. It keeps track of the number of
  // transactions sent from your address and prevents replay attack.

  const nftContract = new alchemyWeb3.eth.Contract(contract.abi, contractAddress);  

  const nonce = await alchemyWeb3.eth.getTransactionCount(
    METAMASK_PUBLIC_KEY,
    "latest"
  );

  const tx = {
    from: METAMASK_PUBLIC_KEY, // your metamask public key
    to: contractAddress, // the smart contract address we want to interact with
    nonce: nonce, // nonce with the no of transactions from our account
    gas: 1000000, // fee estimate to complete the transaction

    data: nftContract.methods
      .createNFT(newOwner, tokenURI) // "0xd0047e035D8ba9B11f45Fa92bD4F474fa191e621" - newOwner
      .encodeABI(), // call the createNFT function from our OsunRiverNFT.sol file
  };

  const signPromise = alchemyWeb3.eth.accounts.signTransaction(
    tx,
    METAMASK_PRIVATE_KEY
  );
  try {
    const result = await signPromise;
    console.log(result)
    const send_signed = await alchemyWeb3.eth.sendSignedTransaction(result.rawTransaction)
    console.log(send_signed)
    return {status: true, contract: send_signed}
  } catch (e) {
    console.log(e)
    return {status: true, contract: null, error: e}
  }

  return signPromise
    .then((signedTx) => {
      alchemyWeb3.eth.sendSignedTransaction(
        signedTx.rawTransaction,
        function (err, hash) {
          if (!err) {
            console.log(
              "The hash of your transaction is: ",
              hash,
              "\nCheck Alchemy's Mempool to view the status of your transaction!"
            );
            return {status: true, contract: hash}
          } else {
            console.log(
              "Something went wrong when submitting your transaction:",
              err
            );
            return {status: false, contract: null, error: err}
          }
        }
      );
    })
    .catch((err) => {
      console.log(" Promise failed:", err);
      return {status: false, contract: null, error: err}
    });
    return {status: false, contract: null, error: null}
}

//mintNFT("https://ipfs.io/ipfs/Qmbs9mANDvu7bs3Nw7aFMGxAnAPces5r1UazwpyhfePUqr") // pass the CID to the JSON file uploaded to Pinata