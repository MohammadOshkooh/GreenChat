web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=config.settings -v2
release: python manage.py migrate
web: python manage.py runserver 0.0.0.0:8000