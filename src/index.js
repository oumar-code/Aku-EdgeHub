const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

app.get('/', (req, res) => {
  res.send('Edge Hub service is running!');
});

app.listen(port, () => {
  console.log(`Edge Hub service listening on port ${port}`);
});
