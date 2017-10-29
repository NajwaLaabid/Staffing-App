Run the server with the following command line
`python manage.py runserver`

Deploy staticfiles
`python manage.py collectstatic`

Start an app
`python manage.py startapp APP_NAME`

In case Github does not wanna proceed with the add & commit
`rm ./.git/index.lock`

migrate db after creating the Models
`python manage.py makemigrations dashboard`
