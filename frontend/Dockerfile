FROM node:7.2.0
COPY package.json bower.json /static/
WORKDIR /static/
COPY entrypoint.sh /entrypoint.sh
RUN npm install -g bower gulp