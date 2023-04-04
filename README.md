# TaxiApp [WIP]

TaxiApp is a real-time taxi application that enables users to request a ride and track their driver's progress in real-time. Built with Django, Django
Channels, and React

# Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python](https://www.python.org/) ( 3.6+)
- [PostgreSQL](https://www.postgresql.org/) (10.1 +)
- [Redis](https://redis.io/) (5.0.0 +)

# Installation

- Clone the repository
- Install dependencies

```bash
$ cd taxiapp
$ pip install -r requirements.txt
$ npm install
```

- Create a `.env` file in the root directory and add environment variables

```bash
$ cp env.example .env
```

- Run the application

```bash
$ docker-compose up
```
