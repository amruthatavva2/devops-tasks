const express = require("express");

const app = express();
const port = process.env.PORT || 8080;

app.get("/", (request, response) => {
  response.send("<h1>Hello World from Docker multi-stage build</h1>");
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
