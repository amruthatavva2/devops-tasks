const express = require('express'); const app = express(); app.get('/health', (_, r) => r.json({status:'secure'})); app.listen(3000);
