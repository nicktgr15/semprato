## Semprato 

Semantic Participatory Journalism Platform 

### How to run

- build image `DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose build --no-cache`
- run `DOCKER_DEFAULT_PLATFORM=linux/amd64 AWS_ACCESS_KEY_ID='' AWS_SECRET_ACCESS_KEY='' API_KEY='' docker-compose up`
- hit `localhost:8083`

note: data gets deleted (including newly created users) every time the container is destroyed 

![alt text](https://raw.githubusercontent.com/nicktgr15/semprato/master/semprato.png)
