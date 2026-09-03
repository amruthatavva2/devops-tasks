# Stage 1: install application dependencies.
FROM node:24-alpine AS builder

WORKDIR /app
COPY package.json ./
RUN npm install
COPY server.js ./

# Stage 2: create the smaller production image.
FROM node:24-alpine AS production

WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY --from=builder /app/server.js ./

EXPOSE 8080
CMD ["npm", "start"]
