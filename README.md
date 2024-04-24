## Тестовое задание
Задача находится в папке ```src/task```

## Запуск приложения

Чтобы собрать и запустить приложение, используйте Docker. Выполните следующие команды из корневой директории проекта:

```bash
# build образа
docker build -t deposit-api .

# запуск контейнера
docker run --rm --name deposit_ruchkin_oleg_testovoe -p 8000:8000 deposit-api
```


## Запуск тестов

Тесты расположены в папке src/tests. Для их запуска из корневой директории проекта выполните следующую команду:

```bash
python3 -m unittest src/tests/tests.py
```


## Контакты 
telegram: ```@oruchkin```
