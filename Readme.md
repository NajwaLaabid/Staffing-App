Run the server with the following command line
`python manage.py runserver`

Deploy staticfiles
`python manage.py collectstatic`

create super user to access django admin
`python manage.py runserver`

Start an app
`python manage.py startapp APP_NAME`

In case Github does not wanna proceed with the add & commit
`rm ./.git/index.lock`

To cancel a pull update on your local workplace
`git reset .\db.sqlite3`

migrate db after creating the Models
`python manage.py makemigrations <nameofapplication>`
`python manage.py migrate`

automatically populate a model in django
- Create folder fixtures
- Add data in a file inside fixtures. Give it a unique name.
- Run following command:
`python manage.py loaddata <fixturename>`


Link to template
https://adminlte.io/themes/AdminLTE/pages/UI/general.html

