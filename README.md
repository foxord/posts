
## 1. Создание проекта

**Команды:**
```bash
 sudo apt install python3-venv
mkdir exam_project && cd exam_project
python3 -m venv venv
source venv/bin/activate
pip install django python-dotenv whitenoise
django-admin startproject exam_project .
python manage.py startapp <имя_приложения>
```

**Изменить `exam_project/settings.py`:**
- В `INSTALLED_APPS` добавить строку `'<имя_приложения>'`

---

## 2. Модель и миграции

**Изменить `<имя_приложения>/models.py`:**
- Создать класс модели с полями из билета
- Добавить `Meta` с `verbose_name`, `verbose_name_plural`
- Добавить `__str__`
- Добавить `clean()` с проверками из билета
- Добавить `save()` с `self.full_clean()`

**Команды:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 3. Админка

**Изменить `<имя_приложения>/admin.py`:**
- Импорт модели
- Декоратор `@admin.register(<Модель>)`
- Класс `<Модель>Admin(admin.ModelAdmin)`
- `list_display` — кортеж полей для таблицы
- `list_filter` — кортеж полей для фильтров
- `search_fields` — кортеж полей для поиска

---

## 4. Переменные окружения (.env)

**Создать файл `.env` в корне (рядом с `manage.py`)**

**Изменить `exam_project/settings.py`:**
- В начало добавить:
  ```python
  import os
  from dotenv import load_dotenv
  load_dotenv()
  ```
- `SECRET_KEY = os.getenv('SECRET_KEY')`
- `DEBUG = os.getenv('DEBUG', 'False') == 'True'`
- `ALLOWED_HOSTS = ['127.0.0.1', 'localhost']`

---

## 5. Middleware метрик

**Создать `<имя_приложения>/middleware.py`**

**Изменить `exam_project/settings.py`:**
- В список `MIDDLEWARE` добавить в конец:
  ```python
  '<имя_приложения>.middleware.MetricsMiddleware'
  ```

---

## 6. Статические файлы (whitenoise)

**Изменить `exam_project/settings.py`:**
- В `MIDDLEWARE` после `SecurityMiddleware` добавить:
  ```python
  'whitenoise.middleware.WhiteNoiseMiddleware'
  ```
- Внизу файла добавить:
  ```python
  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
  ```

**Команда:**
```bash
python manage.py collectstatic
```

---

## 7. URL-роутинг

### 7.1. Создать `<имя_приложения>/urls.py`

Это **локальные** URL приложения. Здесь пишутся маршруты без префикса:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.<функция_списка>, name='<модель>_list'),
    path('create/', views.<функция_создания>, name='<модель>_create'),
    path('<int:pk>/update/', views.<функция_редактирования>, name='<модель>_update'),
    path('<int:pk>/delete/', views.<функция_удаления>, name='<модель>_delete'),
    path('ping/', views.<функция_ping>, name='ping'),
]
```

| Что здесь | Какой адрес получится |
|-----------|----------------------|
| `path('', ...)` | `/<префикс>/` — главная страница списка |
| `path('create/', ...)` | `/<префикс>/create/` — создание |
| `path('<int:pk>/update/', ...)` | `/<префикс>/1/update/` — редактирование объекта с id=1 |
| `path('<int:pk>/delete/', ...)` | `/<префикс>/1/delete/` — удаление объекта с id=1 |
| `path('ping/', ...)` | `/<префикс>/ping/` — тестовый endpoint |

`<int:pk>` — это параметр URL. Django берёт число из адреса и передаёт в view как аргумент `pk`.

### 7.2. Изменить `exam_project/urls.py` (главный файл проекта)

Здесь подключается всё приложение под **одним префиксом**:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<префикс>/', include('<имя_приложения>.urls')),
]
```

| Что здесь | Результат |
|-----------|-----------|
| `path('<префикс>/', include('...'))` | Все URL из `<имя_приложения>/urls.py` получают префикс `/<префикс>/` |

**Пример:** если префикс `employees`, а в приложении `path('ping/', ...)`, то полный адрес: `/employees/ping/`

### 7.3. Тест и URL

Если тест проверяет `/ping/` напрямую, а в главном `urls.py` стоит префикс, тест упадёт с 404. В тесте должен быть полный путь:

```python
response = self.client.get('/<префикс>/ping/')
```

Если нужен `/ping/` без префикса — добавьте отдельно в главный `urls.py`:
```python
path('ping/', views.<функция_ping>),
```

---

## 8. Views

**Изменить `<имя_приложения>/views.py`:**

| Функция | Что делает | Шаблон |
|---------|-----------|--------|
| `<модель>_list` | Берёт все объекты из БД, передаёт в шаблон | `<модель>_list.html` |
| `<модель>_create` | POST — сохраняет форму, GET — показывает пустую форму | `<модель>_form.html` |
| `<модель>_update` | Берёт объект по `pk`, редактирует | `<модель>_form.html` |
| `<модель>_delete` | Берёт объект по `pk`, удаляет по POST | `<модель>_confirm_delete.html` |
| `ping` | Возвращает `JsonResponse({"status": "ok"})` | нет |

Для 404 использовать `get_object_or_404(<Модель>, pk=pk)`.

---

## 9. Форма

**Создать `<имя_приложения>/forms.py`:**
- Класс `<Модель>Form(forms.ModelForm)`
- Внутри `Meta`: `model = <Модель>`, `fields = [...]`
- `widgets` — для Bootstrap-классов (опционально)

---

## 10. Шаблоны

### 10.1. Где создавать папки

```
<имя_приложения>/
├── templates/
│   ├── 404.html                    ← системный шаблон (без подпапки)
│   └── <имя_приложения>/           ← подпапка — namespace
│       ├── base.html
│       ├── <модель>_list.html
│       ├── <модель>_form.html
│       └── <модель>_confirm_delete.html
```

**Почему подпапка `<имя_приложения>` внутри `templates/`?**

Django ищет шаблоны по пути `<имя_приложения>/<шаблон>.html`. Подпапка — это **namespace**: если в двух приложениях есть `base.html`, Django не запутается, потому что пути разные: `employees/base.html` и `products/base.html`.

### 10.2. Как view обращается к шаблону

```python
return render(request, '<имя_приложения>/<шаблон>.html', {...})
```

**Пример:** `render(request, 'employees/employee_list.html', {'employees': employees})`

Django ищет файл по пути:
1. Все папки из `TEMPLATES['DIRS']`
2. В `employees/templates/` (потому что `APP_DIRS = True`)
3. Внутри находит `employees/employee_list.html`

### 10.3. Как шаблоны наследуются

**`base.html`** — родительский шаблон:
```html
{% block title %}{% endblock %}
{% block content %}{% endblock %}
```

**Дочерний шаблон** (например, `employee_list.html`):
```html
{% extends '<имя_приложения>/base.html' %}
{% block title %}...{% endblock %}
{% block content %}...{% endblock %}
```

`{% extends %}` должен указывать полный путь с namespace: `<имя_приложения>/base.html`.

### 10.4. Ссылки в шаблонах

```html
{% url '<имя_маршрута>' %}
{% url '<имя_маршрута>' <объект>.id %}
```

Имя маршрута берётся из `name='...'` в `urls.py` приложения.

| В `urls.py` приложения | В шаблоне |
|------------------------|-----------|
| `name='employee_list'` | `{% url 'employee_list' %}` |
| `name='employee_update'` | `{% url 'employee_update' employee.id %}` |

---

## 11. Тест

**Изменить `<имя_приложения>/tests.py`:**
- Класс `HealthCheckTest(TestCase)`
- Метод `test_ping_endpoint`
- `self.client.get('/<префикс>/ping/')` — полный URL с префиксом
- `self.assertEqual(response.status_code, 200)`

**Команда:**
```bash
python manage.py test
```

---

## 12. Запуск

**Команды:**
```bash
python manage.py createsuperuser
python manage.py runserver
```
