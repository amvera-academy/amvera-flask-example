# Flask на Amvera

Простой пример деплоя Flask в [Amvera](https://amvera.ru/flask).

Это тестовое приложение показывает работу API, шаблона, статических файлов и персистентное сохранение SQlite в постоянное хранилище Amvera.

[КАК СОХРАНЯТЬ БД](#как-правильно-сохранять-бд) | [СТАТИЧЕСКИЕ ФАЙЛЫ](#статические-файлы) | [CELERY](https://github.com/amvera-academy/amvera-fastapi-example/blob/main/CELERY.md) | [КАК ЗАПУСТИТЬ НА AMVERA](#деплой-в-amvera)

## Демо-приложение

Приложение имеет веб-интерфейс, на котором вы сразу можете выполнить доступные тестовые запросы.

- `GET /api/health`
- `GET /api/items`
- `POST /api/items`
- `DELETE /api/items/{id}`

Все запросы можно выполнить на главной странице.

<img width="872" height="883" alt="Screenshot_2" src="https://github.com/user-attachments/assets/d707c40d-f651-483f-8867-8d5aa95210ea" />

## Как правильно сохранять БД

В разработке очень важно учитывать, что любые изменяемые в процессе работы приложения файлы (базы данных, списки, которые нужно сохранять, JSON и т.п.) **необходимо сохранять в [постоянное хранилище Amvera](https://docs.amvera.ru/applications/storage.html#data)**.

Здесь нет ничего сложного: вместо сохранения БД в той же папке, что код, ее нужно сохранять по пути `/data` (это значение по умолчанию, его можно сменить во вкладке "Конфигурация" вашего проекта).

Например:

```python
DATA_DIR = Path("/data")
DATABASE_PATH = DATA_DIR / "items.sqlite3"

def connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection
```

## Статические файлы

Файлы находятся в директории static. Flask раздает их автоматически, а путь в шаблоне создается через `url_for`.

Пример:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}" />
```

## Локальный запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python3 app.py
```

Откройте localhost:5000.

# Flask на Amvera

Простой пример деплоя Flask в [Amvera](https://amvera.ru).

Это тестовое приложение показывает работу API, шаблона, статических файлов и персистентное сохранение SQlite в постоянное хранилище Amvera.

[КАК СОХРАНЯТЬ БД](#как-правильно-сохранять-бд) | [СТАТИЧЕСКИЕ ФАЙЛЫ](#статические-файлы) | [CELERY](https://github.com/amvera-academy/amvera-fastapi-example/blob/main/CELERY.md) | [КАК ЗАПУСТИТЬ НА AMVERA](#деплой-в-amvera)

## Демо-приложение

Приложение имеет веб-интерфейс, на котором вы сразу можете выполнить доступные тестовые запросы.

- `GET /api/health`
- `GET /api/items`
- `POST /api/items`
- `DELETE /api/items/{id}`

Все запросы можно выполнить на главной странице.

## Как правильно сохранять БД

В разработке очень важно учитывать, что любые изменяемые в процессе работы приложения файлы (базы данных, списки, которые нужно сохранять, JSON и т.п.) **необходимо сохранять в [постоянное хранилище Amvera](https://docs.amvera.ru/applications/storage.html#data)**.

Здесь нет ничего сложного: вместо сохранения БД в той же папке, что код, ее нужно сохранять по пути `/data` (это значение по умолчанию, его можно сменить во вкладке "Конфигурация" вашего проекта).

Например:

```python
DATA_DIR = Path("/data")
DATABASE_PATH = DATA_DIR / "items.sqlite3"

def connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection
```

## Статические файлы

Файлы находятся в директории static. Flask раздает их автоматически, а путь в шаблоне создается через `url_for`.

Пример:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}" />
```

## Локальный запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python3 app.py
```

Откройте localhost:5000.

## Деплой в Amvera

Для деплоя конкретно этого приложения вам понадобится:

1. Создать аккаунт в [Amvera](https://cloud.amvera.ru);
2. Создать обычное приложение в любом регионе;
3. Загрузить в него код репозитория;
4. Во вкладке "Конфигурация" нажать кнопку "Собрать".

Когда приложение будет готово к работе и статус сменится на "Запущено", во вкладке "Домены" можно будет создать бесплатное доменное имя от Амвера.

Отдельный пример фоновой задачи и worker описан в общей [инструкции по Celery](https://github.com/amvera-academy/amvera-fastapi-example/blob/main/CELERY.md).
