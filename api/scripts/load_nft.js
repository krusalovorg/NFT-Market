require("dotenv").config();

const hre = require("hardhat");

let ethers = hre.ethers

const API_URL = process.env.API_URL;

const { createAlchemyWeb3 } = require("@alch/alchemy-web3");

const alchemyWeb3 = createAlchemyWeb3(API_URL);
const contract = require("../artifacts/contracts/OsunRiverNFT.sol/MarketNFT.json");
const METAMASK_PUBLIC_KEY = process.env.METAMASK_PUBLIC_KEY;
const METAMASK_PRIVATE_KEY = process.env.METAMASK_PRIVATE_KEY;
const GAS = process.env.GAS;
//const contractAddress = "0x68512832bDD76E93c421Ae2F2bBDeC9aF401bB44";
module.exports = async function LoadNFT(tokenURI, newOwner, private_key) {
  let [deployer] = await ethers.getSigners();

  if (private_key == "market") {
    private_key = METAMASK_PRIVATE_KEY
  } else {
    //let provider = await ethers.getDefaultProvider('https://eth-rinkeby.alchemyapi.io/v2/iSm7xkVtMVgP85UJEvYOunFRFFmF9xdg');

    const provider = await new ethers.providers.JsonRpcProvider(API_URL);
    console.log(provider)
    deployer = await new ethers.Wallet(private_key, provider);
  }

  const acc_balance = await deployer.getBalance();

  console.log("Deploying contracts with the account:", deployer.address);

  if (acc_balance == 0) {
    return {status: false, contract: null, error: "no_balance:0"}
  }

  console.log("Account balance:", (await deployer.getBalance()).toString());

  const NFT = await ethers.getContractFactory("MarketNFT");

  console.log("Use MarketNFT:",NFT)

  const tor = await NFT.deploy();
  console.log("Contract deployed to address:", tor.address);

  const contractAddress = `${tor.address}`

  //return {status: true, contract: tor.address}

  const nftContract = new alchemyWeb3.eth.Contract(contract.abi, contractAddress);  

  const nonce =
  '0x' + (await alchemyWeb3.eth.getTransactionCount(newOwner) + 1).toString(16)

  /*const nonce = await alchemyWeb3.eth.getTransactionCount(
    METAMASK_PUBLIC_KEY,
    "latest"
  );*/

  const tx = {
    from: newOwner, // your metamask public key
    to: contractAddress, // the smart contract address we want to interact with
    nonce: nonce, // nonce with the no of transactions from our account
    gas: GAS, // fee estimate to complete the transaction

    data: nftContract.methods
      .createNFT(newOwner, tokenURI) // "0xd0047e035D8ba9B11f45Fa92bD4F474fa191e621" - newOwner
      .encodeABI(), // call the createNFT function from our OsunRiverNFT.sol file
  };

  const signPromise = alchemyWeb3.eth.accounts.signTransaction(
    tx,
    private_key
  );
  try {
    const result = await signPromise;
    console.log("1:",result)

    const send_signed = await alchemyWeb3.eth.sendSignedTransaction(result.rawTransaction)
    console.log("2:",send_signed)
    return {status: true, contract: send_signed, hash_block: send_signed.transactionHash}
  } catch (e) {
    console.log(e)
    return {status: false, contract: null, error: e}
  }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}