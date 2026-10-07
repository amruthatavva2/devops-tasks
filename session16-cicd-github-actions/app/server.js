const express = require('express'); const app = express();
app.get('/health', (_, res) => res.json({status: 'ok'}));
app.get('/', (_, res) => res.json({message: 'CI/CD demo'}));
app.listen(process.env.PORT || 3000);
module.exports = app;
