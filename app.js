// app.js
const express = require('express');
const fs = require('fs');
const line = require('@line/bot-sdk');

const config = JSON.parse(fs.readFileSync('./line_config.json', 'utf8'));

const app = express();

app.post('/webhook', line.middleware(config), (req, res) => {
  console.log("Webhook received");
  res.status(200).end(); // ここで LINE に HTTP 200 を返します
});

// 動作確認用のルート
app.get('/', (req, res) => {
  res.send('LINE bot server is running');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
