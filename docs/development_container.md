# Локальный docker контейнер для тестирования API приложения

## Описание

Этот контейнер - это независимый сервер, который использует Werkzeug и Django для функционирования. На этом сервере работает версия приложения backend, которая размещена в локальной директории компьютера. Любые изменения в исходном коде непосредственно влияют на функционирование контейнера.

## Подготовка среды для запуска контейнера

Чтобы начать работу с контейнером необходимо:

### Скачать исходный код

Клонировать репозиторий [backend](https://github.com/car-service-with-geolocation/backend) в локальную директорию:

Используя https протокол:

```shell
git clone https://github.com/car-service-with-geolocation/backend.git
```

Либо используя SSH протокол:

```shell
git clone git@github.com:car-service-with-geolocation/backend.git
```

### Установить Docker на локальный компьютер

Инструкции по установке Docker в вашей операционной системе можно найти на [официальном веб сайте Docker](https://docs.docker.com/get-docker/).

### Создать файл .env

Чтобы установить системные переменные, вы должны скопировать файл `.env.template` в файл `.env`.

В Linux и MacOS:

```shell
cp .env.template .env
```

В Windows:

```powershell
Copy-Item -Path <Путь к .env.template> -Destination <Путь к .env>
```

## Сборка и первый запуск контейнера

Для того чтобы собрать и запустить контейнер выполните следующую команду docker-compose:

```shell
docker compose -f docker-compose.dev.yml up -d
```

Вы также можете запустить Docker-compose через приложение Docker Desktop или используя расширение Docker для VS Code.

Будет создан и запущен контейнер с именем `car-dev-server`. Сервис будет назван `dev-server`.

Сервер будет работать по ссылке: `https://127.0.0.1:8000`.

## Работа с контейнером

### Миграция базы данных

Для миграции базы данных выполните команды:

```shell
docker exec -i car-dev-server python manage.py makemigrations
docker exec -i car-dev-server python manage.py migrate
docker exec -i car-dev-server python manage.py import_city
docker exec -i car-dev-server python manage.py import_autoservice
docker exec -i car-dev-server python manage.py import_user
```

### Создание вашего пользователя

Чтобы создать суперпользователя для проверки подлинности и использования Django Admin, вам нужно выполнить следующую команду:

```shell
docker exec -it car-dev-server python manage.py createsuperuser
```

Для пользователя необходимо получить токен аутентификации и добавить его в заголовок вашего запроса в Postman. Для получения токена выполните следующую команду:

```shell
docker exec -i car-dev-server python manage.py drf_create_token <Почта созданного вами ранее пользователя>
```

### Запуск, перезапуск и остановка контейнера

Для запуска, перезапуска и остановки контейнера рекомендуется использовать команды Docker Compose:

**Запуск:**

```shell
docker compose -f docker-compose.dev.yml start
```

**Перезапуск:**

```shell
docker compose -f docker-compose.dev.yml restart
```

**Остановка:**

```shell
docker compose -f docker-compose.dev.yml stop
```

## Заключение

Чтобы узнать больше о Docker, обратитесь к [официальному сайту документации Docker](https://docs.docker.com/).
