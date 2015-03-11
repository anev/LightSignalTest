##### Requirements

You need  `git` and `docker` to run the application. 
Alternatively you can use `python 2.7` and run `Light.py` by your own.

You need `python 2.7` to run tests.

Task described [here](http://machinezone.ru/challenges/traffic-light)

##### Preparing service
 
 Install `git` and `docker` on and run those commands
 
```
git clone https://github.com/anev/LightSignalTest.git # clone the repo
cd LightSignalTest # go into
docker build --tag anev-light-i . # Build docker container
docker run --name anev-light -d -p 80:5000 anev-light-i # run it for the first time!
```

The service will started, you can check it `curl http://localhost/clear`

##### Starting service

To start service after stopping use `docker start anev-light`

##### Stopping service

`docker stop anev-light`

##### Runing tests

`python Tests.py`
