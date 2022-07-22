web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=config.settings -v2
web: gunicorn chatbot.asgi --preload --log-file -
release: python manage.py migrate