<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [ttime](#ttime)
  - [Introduction](#introduction)
  - [Usage](#usage)
    - [Docker image](#docker-image)
      - [Option  one. Get the last built image from Docker Hub repository](#option--one-get-the-last-built-image-from-docker-hub-repository)
      - [Option  two. Build the image by yourself](#option--two-build-the-image-by-yourself)
    - [Run Docker](#run-docker)
    - [call REST service](#call-rest-service)
      - [with curl:](#with-curl)
      - [with swagger](#with-swagger)
  - [Authors](#authors)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->



# ttime

## Introduction
This project implement the web services for calculating travel time



## Usage
Make sure you have `docker` installed

### Docker image

#### Option  one. Get the last built image from Docker Hub repository

```
docker pull ingv/ttime:latest
```



#### Option  two. Build the image by yourself

```
git clone https://gitlab+deploy-token-145:spGK6LimgbJhetYr5VDN@gitlab.rm.ingv.it/docker/ttime.git
cd ttime
docker build --tag ingv/ttime .
```



### Run Docker 

staying inside `ttime` folder ...

```
docker run -it --name flask_ttime -p [YOUR-PORT]:5000 -d --user $(id -u):$(id -g) --rm ingv/ttime
docker exec -i flask_ttime tail -f /opt/log/ttime.log
```

### call REST service

#### with curl:

```
curl "http://[HOST]:[YOUR-PORT]/api/get_phase_circle?lat=35&lon=12&depth=33&time=200&phase=P&azimuth_interval=90"

```

#### with swagger

from web browser ...

```
http://[HOST]:[YOUR-PORT]
```




## Authors
(c) 2021 Sergio Bruni sergio.bruni[at]ingv.it, Fabrizio Bernardi fabrizio.bernardi[at]ingv.it, Valentino Lauciani valentino.lauciani[at]ingv.it

Istituto Nazionale di Geofisica e Vulcanologia, Italia