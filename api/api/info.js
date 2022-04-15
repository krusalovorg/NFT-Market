const express = require('express');
const router = express.Router();

const GAS = process.env.GAS;
const PASS = process.env.PASS;

router.post('/info', function(req, res) {
    try {
        const { password } = req.body;

        if (password == PASS) {
            res.json({
                gas: GAS,
            })
            return;
        } else {
            res.status(404)
        }
    } catch (e) {
        console.log(e.message)
        console.log(e)
        res.status(500).json({ message : "Something went wrong, try again"})
    }
});

module.exports = router;