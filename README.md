# Йәнтөйәк

Веб-платформа для сохранения и популяризации локальных географических названий (топонимов) Башкортостана.

## О проекте

Проект собирает и отображает местные названия природных объектов (урочища, горы, родники, скалы, хребты и т.д.), которые известны в основном старшему поколению и постепенно исчезают из речи.

**Текущий статус:** MVP в разработке. Основной функционал — каталог топонимов и интеграция с картой Google My Maps.

## Технологический стек

- **Бэкенд:** Django 5.2 (Python 3.13)
- **Фронтенд:** Django Templates + Bootstrap 5
- **База данных:** PostgreSQL
- **Карта:** Google My Maps (встраивается через iframe / ссылку)
- **Хранение медиа:** локальная папка `media/`

## Структура проекта


## Модель Toponym

Основная сущность — топоним. Поля:

- `name_bash`, `name_rus` — названия на башкирском и русском
- `type` — тип объекта (гора, родник, урочище, скала и т.д.)
- `latitude`, `longitude` — координаты
- `description` — описание/легенда
- `photo`, `audio` — медиа
- `reg_number`, `map_nomenclature` — служебные данные из реестра АГКГН
- `status` — черновик / на модерации / опубликовано / спорный / отклонено
- `votes_for`, `votes_against` — для голосований
- `created_by`, `created_at`, `updated_at` — метаданные

## Данные

Исходный датасет — **3 867 точечных топонимов**, извлечённых из официального реестра АГКГН (Росреестр) для Республики Башкортостан. Реки, озёра и населённые пункты исключены (они уже есть на обычных картах).

Файлы:
- `toponyms_filtered_final.csv` — русскоязычная версия
- `toponyms_for_google.csv` — с колонками `Latitude`/`Longitude` для импорта в Google My Maps

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Niyaz0912/yantoyak.git
cd yantoyak

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

pip install django~=5.0 psycopg2-binary python-dotenv Pillow pdfplumber pandas openpyxl

DB_NAME=yantoyak
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

YANDEX_MAPS_API_KEY=your_yandex_key
createdb -U postgres yantoyak
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver