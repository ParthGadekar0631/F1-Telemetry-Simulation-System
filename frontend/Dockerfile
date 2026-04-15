FROM node:20-alpine

WORKDIR /usr/src/app

COPY package.json tsconfig.json tsconfig.app.json tsconfig.node.json vite.config.ts index.html ./
RUN npm install

COPY src ./src
COPY public ./public

RUN npm run build

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]
