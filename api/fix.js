const mintNFT = require('./scripts/mint-nft')

mintNFT('0xb09A98b93DbB627e16E8C875E452CcfB8Ac2A54F',
'https://ipfs.io/ipfs/Qmbs9mANDvu7bs3Nw7aFMGxAnAPces5r1UazwpyhfePUqr',
'0xd0047e035D8ba9B11f45Fa92bD4F474fa191e621')

// const API_URL = process.env.API_URL;

// const { createAlchemyWeb3 } = require("@alch/alchemy-web3");

// const alchemyWeb3 = createAlchemyWeb3(API_URL);
// const value = "0xf9012918843b9acfe8830f424094a17e371c7a4ef85a8197af450041484141ea673180b8c4a5614033000000000000000000000000d0047e035d8ba9b11f45fa92bd4f474fa191e6210000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000004368747470733a2f2f697066732e696f2f697066732f516d6273396d414e447675376273334e773761464d4778416e415063657335723155617a7770796866655055717200000000000000000000000000000000000000000000000000000000002ca05bfdd853db00443770a0c4d66883312333261005c8610eb7dafbc5d0a6466464a064d196b72202405faa53b4d74ff16c69efcc85570bc1123ee48f0eacb8c537a4"
// const send_signed = alchemyWeb3.eth.sendSignedTransaction(value)
// console.log(send_signed)