require("dotenv").config();
const API_URL = process.env.API_URL;
const { createAlchemyWeb3 } = require("@alch/alchemy-web3");
const alchemyWeb3 = createAlchemyWeb3(API_URL);
const contract = require("../artifacts/contracts/OsunRiverNFT.sol/TorNFT.json");
const METAMASK_PUBLIC_KEY = process.env.METAMASK_PUBLIC_KEY;
const METAMASK_PRIVATE_KEY = process.env.METAMASK_PRIVATE_KEY;
const contractAddress = "0x68512832bDD76E93c421Ae2F2bBDeC9aF401bB44"; // the hash of the smart contract to be used in minting this NFT
const nftContract = new alchemyWeb3.eth.Contract(contract.abi, contractAddress);

async function mintNFT(tokenURI) {
  // get the nonce - nonce is needed for security reasons. It keeps track of the number of
  // transactions sent from your address and prevents replay attack.
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
      .createNFT("0xd0047e035D8ba9B11f45Fa92bD4F474fa191e621", tokenURI)
      .encodeABI(), // call the createNFT function from our OsunRiverNFT.sol file
  };

  const signPromise = alchemyWeb3.eth.accounts.signTransaction(
    tx,
    METAMASK_PRIVATE_KEY
  );
  signPromise
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
          } else {
            console.log(
              "Something went wrong when submitting your transaction:",
              err
            );
          }
        }
      );
    })
    .catch((err) => {
      console.log(" Promise failed:", err);
    });
}

mintNFT("https://ipfs.io/ipfs/Qmbs9mANDvu7bs3Nw7aFMGxAnAPces5r1UazwpyhfePUqr") // pass the CID to the JSON file uploaded to Pinata