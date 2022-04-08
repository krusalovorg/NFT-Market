const express = require('express')
const bodyParser = require('body-parser')

const app = express()
const jsonParser = bodyParser.json({limit: "50mb"})
const urlencodedParser = bodyParser.urlencoded({ extended: false, limit: "50mb" })

const port = 3000

app.use(jsonParser)
app.use(urlencodedParser)

app.use("/api", require("./api/create_nft"))

app.listen(port, () => {
  console.log(`Api server started on port ${port}`)
})