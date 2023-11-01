# Facebook Clonse build in Python and MySQL database
MAKE SURE TO INSTALL IT IN VIRTUAL ENVIRONMENT
The project is not complete and there will be bugs and unfinished pages.
It will be updated every day, make sure you have **MySQL** installed.

# SETUP GUIDE
     git clone https://github.com/Dachii11/Facebook-Clone-Using-Django.git
     cd Facebook-Clone-Using-Django
   
     pip install -r requirements.txt
     python manage.py makemigrations
     python manage.py migrate
     python manage.py createsuperuser
     python manage.py runserver

# In your fb/settings.py add your email.
     ```
     EMAIL_HOST_USER = 'your_email_address'
     EMAIL_HOST_PASSWORD = 'your_password'
     ```
