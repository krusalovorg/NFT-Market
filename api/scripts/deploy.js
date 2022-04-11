const hre = require("hardhat");

const ethers = hre.ethers


module.exports = async function Deploy() {
    const [deployer] = await ethers.getSigners();
    const acc_balance = await deployer.getBalance();

    console.log("Deploying contracts with the account:", deployer.address);

    if (acc_balance == 0) {
      return {status: false, contract: null, error: "no_balance:0"}
    }

    console.log("Account balance:", (await deployer.getBalance()).toString());

    const NFT = await ethers.getContractFactory("MarketNFT");

    // Start deployment, returning a promise that resolves to a contract object
    const tor = await NFT.deploy();
    console.log("Contract deployed to address:", tor.address);

    return {status: true, contract: tor.address}
 }

 /*main()
   .then(() => process.exit(0))
   .catch(error => {
     console.error(error);
     process.exit(1);
   });*/
