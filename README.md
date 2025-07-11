# Сервис анализа жалоб пользователей

## Общая информация

Сервис анализа разработан на основе фреймворка **FastAPI, СУБД PostgreSQL, миграции Alembic**. Основой взаимодействия с БД является паттерн ***UnitOfWork***, что позволяет абстрактно и гибко взаимодействовать с БД.
**Анализ обращений** выполняется посредством запросам к *API* следующих сервисов:
* **Анализ тональности текста** - [API Layer Sentiment](https://apilayer.com/marketplace/sentiment-api). 
 **!ОГРАНИЧЕНИЕ** - Данный API работает только с английским текстом - при работе с русским языком возвращает `500 Internal Server Error`
* **Анализ категории** - Может работать с любой **OpenAI** реализацией, однако использован [OpenRouterAPI](https://openrouter.ai), включающий большое количество моделей.
* **Определение местоположения** - [IP-API](http://ip-api.com)

## Структура проекта

```
. # Предполагается, что у нас развернута целая система по обслуживанию ресторана
├── environments          # Переменные окружения сервисов/
│   └── hightalent_reservation/
│       └── .env.production
├── hightalent_reservation/ # Сервис для бронирования столиков
│   ├── app/
│   │   ├── api               # Папка хранения API всех роутеров и Зависимостей/
│   │   │   ├── routers.py
│   │   │   └── dependencies.py
│   │   ├── database          # Здесь лежит основной (общий) репозиторий по паттерну UnitOfWork
│   │   ├── migrations        # Миграции alembic
│   │   ├── modules           # Модули сервиса/
│   │   │   ├── reservation       # Модуль бронирования столиков/
│   │   │   │   ├── models            # Модели БД
│   │   │   │   ├── schemas           # Схемы pydantic
│   │   │   │   ├── router.py         # API-роутер модуля
│   │   │   │   ├── service.py        # Функции для взаимодействия с репозиторием по бронированию столиков
│   │   │   │   └── uow.py            # Репозиторий бронирования столиков
│   │   │   └── # По такому же принципу можно вставлять любой модуль
│   │   ├── exceptions.py    # Исключения сервиса
│   │   ├── main.py          # Корень запуска проекта, содержащий middleware и включение всех роутеров
│   │   ├── settings.py      # Файл конфигурации сервиса и сервисов-соседей
│   │   ├── unitofwork.py    # Абстрактный класс к репозиториям для взаимодействия с БД
│   │   └── utils.py  
│   ├── .gitignore
│   └── startup.sh
└── docker-compose.yaml   
```

## Требования:

* **Python 3.12**
* **Docker**
* **Docker-compose**
* **PostgreSQL**
* **Poetry**

## Запуск сервиса

Клонирование сериса:

```
git clone https://github.com/YourCarma/hightalent_reservation.git
```

### Запуск сервиса вручную

Переходим в папку проекта:

`cd hightalent_reservation`

Проверьте **переменные окружения** в `.env.production`!

**Убедитесь** в доступности **PostgreSQL**!

**Установка** зависимостей:

`poetry install`

**Активация** виртуального окружения:

`poetry shell`

**Миграции** БД:

`alembic upgrade head`

Далее **запускаем** сервис:

```
cd app
python main.py
```

**Сервис запущен!** Теперь можно посмотреть документацию **OpenAPI** `http://{HOST}:{PORT}/docs`

![1744897247162](image/README/1744897247162.png)

### Запуск сервиса с помощью docker-compose

`docker-compose.yaml` состоит из трех контейнеров:

1. `reservation-service` - сам сервис бронирования столиков
2. `postgres` - СУБД PostgreSQL
3. `portainer` - Portainer для графического взаимодействия

Запускаем сервисы:

`docker-compose up -d`

Выполняем миграции БД:

`docker-compose exec reservation-service alembic upgrade head`

1. Заходим в [portainer](http://localhost:9000 "ссылка на portainer")
2. Создаем пользователя
3. Авторизируемся
4. Наблюдаем наши сервисы
5. **Готово!**

   ![1744894111115](hightalent_reservation/image/README/1744894111115.png)