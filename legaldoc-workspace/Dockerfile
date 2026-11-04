FROM node:22-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund
COPY server.js schema.sql workspace.html workspace.js workspace.css ./
ENV NODE_ENV=production
EXPOSE 3000
CMD ["node","server.js"]
