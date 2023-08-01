# YaMDB API
## Описание
YaMDB API предоставляет интерфейс для работы с системой рейтинга произведений YaMDB: каждый пользователь имеет возможность оставить отзыв о произведении и поставить ему оценку. Кроме того, каждый пользователь может комментировать отзывы.
## Установка
- Клонируйте проект из гитхаба:  
`git clone git@github.com:s1owp0k3r/api_yamdb.git`
- Создайте и активируйте виртуальное окружение:  
`python -m venv venv`  
`source venv/Scripts/activate`
- Установите зависимости из файла requirements.txt:  
`pip install -r requirements.txt`
- Примените миграции:
`python manage.py migrate`
- Запустите сервер:  
`python manage.py runserver`
## Примеры запросов
- POST /api/v1/auth/signup/ - Регистрация нового пользователя.
- POST /api/v1/auth/token/ - Получение JWT-токена.
- GET /api/v1/titles/ - Получить список всех произведений.
- POST /api/v1/titles/ - Добавление нового произведения в коллекцию (доступно только администратору).
- GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов на произведение.
- POST /api/v1/titles/{title_id}/reviews/ - Добавление нового отзыва на произведение.
- PATCH /api/v1/titles/{title_id}/reviews/{review_id}/ - Редактирование (частичное обновление) отзыва по id.
- DELETE /api/v1/titles/{title_id}/reviews/{review_id}/ - Удаление отзыва по id.
- GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву.
- POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Добавление комментария к отзыву.
- GET /api/v1/users/ - Получение списка всех пользователей (доступно только администратору).
- POST /api/v1/users/ - Добавление нового пользователя (доступно только администратору).
- PATCH /api/v1/users/me/ - Изменение данных своей учетной записи.
## Авторы
Команда проекта:
- Борис Градов
- Алексей Дубовской
- Денис Ванеев
## Используемые технологии
Проект создан с использованием Django Rest Framework, аутентификация пользователей осуществляется через jwt-токены.