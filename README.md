<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [ttime - Travel Time](#ttime---travel-time)
  - [Introduction](#introduction)
  - [Quickstart](#quickstart)
    - [Get Docker image](#get-docker-image)
      - [1) Get built image from DockerHub (*preferred*)](#1-get-built-image-from-dockerhub-preferred)
      - [2) Build by yourself](#2-build-by-yourself)
    - [Run as a service](#run-as-a-service)
  - [Test ttime as a stand alone script](#test-ttime-as-a-stand-alone-script)
  - [Contribute](#contribute)
  - [Authors](#authors)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

[![License](https://img.shields.io/github/license/INGV/ttime.svg)](https://github.com/INGV/ttime/blob/main/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/INGV/ttime.svg)](https://github.com/INGV/ttime/issues)

[![Docker build](https://img.shields.io/badge/docker%20build-from%20CI-yellow)](https://hub.docker.com/r/ingv/ttime)![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/ingv/ttime?sort=semver)![Docker Pulls](https://img.shields.io/docker/pulls/ingv/ttime)

[![CI](https://github.com/INGV/ttime/actions/workflows/docker-image.yml/badge.svg)](https://github.com/INGV/ttime/actions)[![GitHub](https://img.shields.io/static/v1?label=GitHub&message=Link%20to%20repository&color=blueviolet)](https://github.com/INGV/ttime)

# ttime - Travel Time

## Introduction
This project implement the web services to calculate travel time

## Quickstart
### Get Docker image
To obtain *ttime* docker image, you have two options:

#### 1) Get built image from DockerHub (*preferred*)
Get the last built image from DockerHub repository:
```sh
docker pull ingv/ttime:latest
```

#### 2) Build by yourself
Clone the git repositry:
```sh
git clone https://github.com/INGV/ttime.git
cd ttime
```
build the image:
```sh
docker build --tag ingv/ttime . evaluator
```

in case of errors, try:
```sh
docker build --no-cache --pull --tag ingv/ttime . 
```

### Run as a service
run the container in daemon (`-d`) mode:
```
docker run -it --rm --name flask_ttime -p 8383:5000 -d --user $(id -u):$(id -g) ingv/ttime
docker exec -i flask_ttime tail -f /opt/log/ttime.log
```

Then test access to: http://localhost:8383/Contribute

Examples of URL:

- http://localhost:8383/api/get_phase_circle?lat=45.492599&lon=9.19289&depth=50&time=100&phases=P%2CS&azimuth_interval=30



## Test ttime as a stand alone script

If you have cloned the project, you can check the evaluator engine from command line.
To do this you need *python3.x* installed on your machine and also some python libraries:

```sh
pip install -r requirements.txt
python main/api/queries.py --help
```

Here is some examples of launch:

```sh
python main/api/queries.py --lat 35 --lon 10 --depth 50 --time 100 --phases P,S
python main/api/queries.py -l 35 -o 10 -d 50 -t 100 -p P,S -a 30
```



## Contribute

Thanks to your contributions!

Here is a list of users who already contributed to this repository: \
<a href="https://github.com/ingv/ttime/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ingv/ttime" />
</a>

## Authors
(c) 2023 Sergio Bruni sergio.bruni[at]ingv.it \
(c) 2023 Fabrizio Bernardi fabrizio.bernardi[at]ingv.it \
(c) 2023 Valentino Lauciani valentino.lauciani[at]ingv.it

Istituto Nazionale di Geofisica e Vulcanologia, Italia
