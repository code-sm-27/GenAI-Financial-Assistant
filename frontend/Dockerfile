FROM node:20-slim as development

WORKDIR /app
COPY package.json package-lock.json ./

RUN npm install
COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
