
Django-проект лабораторных работ с PostgreSQL-базой `labs1`.

1. Скопируйте `.env.example` в `.env` и укажите пароль PostgreSQL.
2. Установите зависимости: `python -m pip install -r requirements.txt`.
3. Проверьте проект: `python manage.py check`.
4. Запустите: `python manage.py runserver`.

Лабораторные реализуются последовательно в этом репозитории:

- ЛР1: модели, роли, ограничения и миграции;
- ЛР2: ORM-оптимизация, статистика и `EXPLAIN`;
- ЛР3: DRF CRUD, валидация, фильтры и пагинация;
- ЛР4: JWT, разграничение доступа и защита от IDOR;
- ЛР5: `transaction.atomic` и `select_for_update`;
- ЛР6: тесты, Docker Compose и документация.

Проверка: `python manage.py test`.
