FROM node:22-alpine
WORKDIR /app
COPY package.json public-server.js index.html app.html style.css demo-review.js builder.html builder.js builder.css legal-catalog.js governance.html governance.js governance.css governance-templates.js intake.html intake.js intake-flow.js intake.css robots.txt sitemap.xml ./
ENV NODE_ENV=production
EXPOSE 3000
CMD ["node","public-server.js"]
