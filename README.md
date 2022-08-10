# Задание

Что нужно сделать

1. Перевести в poetry и повысить версию Django
2. Сделать проверку на корректный email с помощью сервиса millionverifier
3. Добавить опцию рассылки корректных email заданного сообщения
4. Добавить админку для загрузки файлов Excel 
5. Добавить DRF для загрузки отображения статуса email
6. Добавить модульное тестирование
7. Создать docker-compose.yml для того чтобы разворачивался данный сервис


## 1. Перевести в poetry

poetry - удобный менеджер пакетов

Перевести на последную версию Django

## 2. Проверка на корректный email 

Для проверки использовать следующее api

```
https://api.millionverifier.com/api/v3/?api=N7JIvmPXtNIEruQ3ILd8yAudp&email=<email>&timeout=10
```

## 3. Рассылка

Сообщения рассылать на те email, которые прошли верификация в п.2.

Рассылка должна быть независимой (отдельной) от п.2.

## 4. Добавить админку

Использовать [django admin](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/)

## 5. DRF

На основе [djangorestframework](https://www.django-rest-framework.org/) сделать API, которое будет показывать статус email



## 6. Добавить модульное тестирование

Написать unit testы для

* загрузки excel файла
* верификации
* отправки email
* API

## 7. Docker

Создать docker-compose.yml для развёртывания в среде docker на основе образа (python:3.10-slim-buster)[https://hub.docker.com/_/python]


## 8*. gitlab-ci.yml

Если есть знания, то сделать `.gitlab-ci.yml` для прохождения тестов и flake8 в сервисе gitlab.com

* - необязательное задание