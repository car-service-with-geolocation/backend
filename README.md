# Backend сервиса по поиску ближайшего автосервиса

[Описание работы с локальным докер контейнером приложения](./docs/development_container.md)

## Возможности сервиса:
- сервис позволяет пользователю найти ближайший автосервис по указанным
фильтрам поиска
- позволяет оставить отзыв на автосервис
- (в разработке) пройти регистрацию по номеру телефона или электронной почте
- (в планах проекта) оставить заявку на обслуживание в выбранном автосервисе
- (в планах проекта) хранить историю оформленных заявок на обслуживание в 
личном кабинете пользователя

## Вопросы и трудности при реализации:

### Структура проекта и версионирование API
В данный момент структура Django-приложения состоит из приложений для 
соответствующих моделей и приложение `api`, в котором находтся все файлы 
`urls.py`,`serializers.py,`, `views.py`. Данная структура позволяет быстро
создать новую версию api, но нагромождает проект директориями. Нужна помощь в 
подходе к выбору структуры Django-приложения

### Подключение smtp-сервера для отправки электронных писем
Не удаленном сервере не происходит отправка электронных писем на электронные 
адреса пользователей, локально все работает и письма отправляются. В гитхаб
секреты все необходимые значения для параметров прокинуты для форминрования 
.env-файла на сервере.

### Хранение и передача нескольких картинок для отзывов
Предполагается что в отзывах может быть несколько картинок и указать просто
ImageField не получится, как лучше реализовать этот функционал, через отдельный
класс? Как хранить и быстро искать нужные картинки для выдачи?

## Базовые модели проекта
### Транспорт
Модель для выбора марки автомобиля при фильтрации поиска и указания конкретной 
специализации автосервиса.

Поля модели:
- brand
- slug

### Виды работ
Модель хранит список производимых автосервисами работ, с указанием стоимости 
определенного вида работы для конкретного автосервиса. Также позволяет 
производить фильтрацию по полю при выполнении поиска. Связана с моделью
автосервиса через `AutoserviceJob`.

Поля модели:
- title
- description


### Компания
Хранит информацию о компании владеющей сетью автосервисов. Представляет собой 
не редактируемый личный кабинет компании. В дальнейшем представляет возмодность
сделать полноценный личный кабинет для владельца.

Поля модели:
- title
- description
- logo
- legal_address

### Автосервис
Хранит информацию об автосервисе.

Поля модели:
- company
- address
- geolocation
- city
- working_time_text
- phone_number
- email
- site
- job
- car_service

### WorkingTime
Модель позволяет создать расписание работы автосервиса в разные дни недели

### WorkingTimeRange
Модель позволяет указать временной промежуток работы автосервиса для каждого
дня недели

### Отзыв
Модель позволяет создать отзыв на автосервис. Находится в доработке. На текущий 
момент любой авторизованный пользователь может оставить отзыв на любой сервис.
В будущем будет добавлен функционал позволяющий оставить отзыв только после 
оформления пользователем заявки в выбранный автосервис.

Поля модели:
- author
- autoservice
- text
- score
- pub_date

### Пользователь (нужна помощь с реализацией)
Модель кастомного пользователя. Для работы с пользователями используются
возможности библиотеки Djoser. Для пользователя предусмотрена авторизация по
электронной почте, номеру телефона или никнейму, для этого используется класс
`AuthBackend`. В разработке находится процесс регистрации пользователя по 
телефону или электронной почте. На текущий момент возникают сложности с
сохранением пароля. Предположительное решение проблемы - добавление кастомного
сериализатора для регистрации.

Поля модели:
- username
- email
- last_name
- first_name
- last_name
- phone_number
- date_joined
- image

***
## Manage команды
Выполните команды в следующей последовательности и загрузите данные в БД. import_city - загрузка реальных городов и их координат. import_autoservice - загрузка данных реальных автосервисов и связанных с ними моделей. import_user - загрузка тестовых пользователей.
```
python manage.py import_city
python manage.py import_autoservice
python manage.py import_user
```
