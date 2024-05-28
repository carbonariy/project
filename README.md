# project

Simple service to send a static link (for example to the mobile app) via SMS through SMSC.RU.

#### Run docker composer

```sh
cp backend/app/.env.example backend/app/settings/.env

docker compose up -d --build app
```

The API by default is attached to <http://localhost:8080/api/v1/>

#### Run linters

After build:

```sh
docker compose exec app bash -c "flake8 backend"
docker compose exec app bash -c "cd backend && mypy --config-file ../pyproject.toml ."
```

#### Run tests

```sh
docker compose exec app bash -c "cd backend && pytest"
```