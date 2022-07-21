export DJANGO_SETTINGS_MODULE=config.settings
heroku config:set DJANGO_SETTINGS_MODULE=config.settings --account personal
web: daphne config.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
web: daphne -b 0.0.0.0 -p 8001 config.asgi:application
chatworker: python manage.py runworker --settings=config.settings -v2
release: python manage.py migrate