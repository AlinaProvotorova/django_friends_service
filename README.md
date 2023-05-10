# django_friends_service
Django-сервис друзей


## Запуск приложения:

- Клонируйте репозиторий командой в терминале:

```commandline
...$  git clone https://github.com/AlinaProvotorova/django_friends_service.git
```
- Активируйте виртуальное окружение командой:

```commandline
...$ python -m virtualenv venv && .\venv\Scripts\activate
```

- Установите зависимости командой:

```
(venv) ...$ python3 -m pip install --upgrade pip
```

```
(venv) ...$ pip install -r requirements.txt
```

- Примените миграции:

```
(venv) ...$ python manage.py migrate 
```

- Запустите сервер:

```
(venv) ...$ python manage.py runserver
```

- После запуска перейдите по [ссылке документации Swagger](http://127.0.0.1:8000/swagger)

# API Documentation

## Friends List

Retrieves the list of friends for a user.

- **URL**
  - `/api/friends/`
- **Method**
  - `GET`
- **Success Response**
  - **Code**: 200 OK
  - **Response Body**
    ```json
    [
      {
        "id": 1,
        "user": 1,
        "friend": 2,
        "is_accepted": true
      },
      {
        "id": 2,
        "user": 1,
        "friend": 3,
        "is_accepted": true
      }
    ]
    ```

## Remove Friend

Removes a friend from the user's friend list.

- **URL**
  - `/api/friends/remove/<int:pk>/`
- **Method**
  - `DELETE`
- **Path Parameters**
  - `pk` - ID of the friend to remove
- **Success Response**
  - **Code**: 200 OK
  - **Response Body**
    ```json
    {
      "success": "Friend removed."
    }
    ```

## Friendship Status

Retrieves the friendship status with a specific user.

- **URL**
  - `/api/friends/status/<int:pk>/`
- **Method**
  - `GET`
- **Path Parameters**
  - `pk` - ID of the user to check friendship status with
- **Success Response**
  - **Code**: 200 OK
  - **Response Body**
    ```json
    {
      "friend": {
        "id": 2,
        "username": "friend_user"
      },
      "status": "Already friends"
    }
    ```

## Send Friend Request

Sends a friend request to another user.

- **URL**
  - `/api/friend-request/send/`
- **Method**
  - `POST`
- **Request Body**
  ```json
  {
    "friend": 2
  }
- **Success Response**
  - **Code**: 201 CREATED
  - **Response Body**
    ```json
    {
      "id": 1,
      "user": 1,
      "friend": 2,
      "is_accepted": false
    }
    ```

## Accept Friend Request

Accepts a friend request from another user.

- **URL**
  - `/api/friend-request/accept/<int:pk>/`
- **Method**
  - `PATCH`
- **Path Parameters**
  - `pk` -  ID of the friend request to accept
- **Success Response**
  - **Code**: 200 OK
  - **Response Body**
    ```json
    {
      "success": "Friend request accepted."
    }
    ```

## Reject Friend Request

Rejects a friend request from another user.

- **URL**
  - `/api/friend-request/reject/<int:pk>/`
- **Method**
  - `DELETE`
- **Path Parameters**
  - `pk` -  ID of the friend request to reject
- **Success Response**
  - **Code**: 200 OK
  - **Response Body**
    ```json
    {
      "success": "Friend request rejected."
    }
    ```
    
Автор: [Провоторова Алина Игоревна](https://t.me/alinamalina998)