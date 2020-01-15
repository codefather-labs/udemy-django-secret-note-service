# udemy-django-secret-note-service


## Build
- Instal docker, docker-compose
- Run docker daemon if it not started
- Use this commands in terminal inside project folder:

- docker-compose build
- docker-compose run django python3 /app/manage.py createsuperuser

After that, Django will waiting login, email and password of your superuser account. After creating superuser go next:

## Run
- docker-compose up
- http://0.0.0.0:8005/admin
- use your superuser account login and password

- For now, go https://my.telegram.org/auth and get or create your Telegram application. 
- Add your Telegram application like config in Django admin panel
- Go to http://0.0.0.0:8888 and wait for Telegram session starts! It's need few secs.

- Enjoy! ;)

Special for Udemy with <3
