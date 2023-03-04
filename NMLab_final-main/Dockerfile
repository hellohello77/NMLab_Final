# FROM node:14-alpine AS builder
# WORKDIR /app
# COPY package.json yarn.lock ./
# COPY ./src ./src
# COPY ./public ./public
# RUN yarn install
# RUN yarn build


FROM python:3.8-alpine
# switch working directory
WORKDIR /app
# copy the requirements file into the image
COPY ./requirements.txt ./
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt
# copy every content from the local file to the image
COPY ./gps ./gps
COPY ./build ./build/
COPY ./aws ./aws
COPY ./main.py ./

EXPOSE 4000
# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]
CMD ["main.py" ]