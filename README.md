## Facebook Clone build in Python with MySQL database
**MAKE SURE TO INSTALL IT IN VIRTUAL ENVIRONMENT.**
The project is not complete and there will be lots of bugs and unfinished pages.
It will be updated every day, make sure you have **MySQL** installed.

# SETUP GUIDE
     git clone https://github.com/Dachii11/Facebook-Clone-Using-Django.git
     cd Facebook-Clone-Using-Django
     pip install -r requirements.txt

## In your fb/settings.py add your email.
     ```
     EMAIL_HOST_USER = 'your_email_address'
     EMAIL_HOST_PASSWORD = 'your_password'     # (gmail requires 16 digit app password)
     ```

## Create MySQL database and add it to your fb/settings.py
     ```
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'YOUR_DATABASE_NAME',
             'USER': 'MYSQL_USER',
             'PASSWORD': 'MySQL password', 
             'HOST': 'localhost',
             'PORT': '3306',
              }
     }
     ```
## in Facebook-Clone-Using-Django/ dir, Run command to migrate Database
     python manage.py migrate
     
## command for Create superuser
     python manage.py createsuperuser

## Make sure you have created profile for superuser
     ```
     python manage.py shell
     >>> from django.contrib.auth.models import User
     >>> from accounts.models import Account
     >>> admin = User.objects.get(username='YOUR_SUPERUSER_USERNAME')
     >>> Account.objects.create(user=admin,username=admin.username,id_user=admin.id)
     >>> quit()

**admin** page link: **1KDl0KL_03kffj_jKA_SF0k_l1K03_31KL_KDA/**

## Finally, run the server...
     python manage.py runserver
     
![My Image](FB.png)
