FROM node

WORKDIR /app

COPY  package.json .

RUN npm i

RUN chmod +rw node_modules

COPY  . .

CMD [ "npm", "run", "dev" ]
