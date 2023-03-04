## Installation

**Install packages for python library**

```bash
$ pip3 install -r requirements.txt
```

**Install npm packages**

```bash
$ yarn install
```

## Setup aws

refer to course documentation p.17

## How to run

**Build the frontend first**

```bash
$ yarn build
```

**Start mqtt broker**

```bash
$ docker run -d -it -p 1883:1883 -v $(pwd)/mqtt_protocol/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```

**Start the backend server**

```bash
$ python main.py
```

## How to use

You can access the website according to the ip of your computer or http://localhost:4000

## Deploy

```bash
sudo docker-compose up -d
```

## Update deploy

```bash
sudo touch uwsgi.ini
```