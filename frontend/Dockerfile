FROM node

WORKDIR /app

COPY  package.json .

RUN npm i

COPY  . .

COPY .env .env

CMD [ "npm", "run", "dev" ]
