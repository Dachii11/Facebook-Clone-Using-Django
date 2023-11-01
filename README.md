## Facebook Clonse build in Python with MySQL database
MAKE SURE TO INSTALL IT IN VIRTUAL ENVIRONMENT.
The project is not complete and there will be bugs and unfinished pages.
It will be updated every day, make sure you have **MySQL** installed.

# SETUP GUIDE
     git clone https://github.com/Dachii11/Facebook-Clone-Using-Django.git
     cd Facebook-Clone-Using-Django
     pip install -r requirements.txt

## In your fb/settings.py add your email.
     ```
     EMAIL_HOST_USER = 'your_email_address'
     EMAIL_HOST_PASSWORD = 'your_password'
     ```

## Create MySQL database and add it to your fb/settings.py
     ```
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'YOUR_DATABASE_NAME',
             'USER': 'DATABASE_USER',
             'PASSWORD': 'MySQL password',     // if password is not required remove this line of code.
             'HOST': 'localhost',
             'PORT': '3306',
              }
     }
     ```

## Run commands to migrate Database
     python manage.py makemigrations
     python manage.py migrate

## commands for Create superuser and run server
     python manage.py createsuperuser
     python manage.py runserver
