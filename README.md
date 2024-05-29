#  TaskX Project

## Overview

The **TaskX** project is a task management application developed using Django. It allows users to manage tasks, assign them to other users, and keep track of their tasks.

## Features

1. **🔐 User Authentication**:
   - Registration, login, and logout functionality.
   - Only authenticated users can create, update, and delete tasks.

2. **🗂️ Task Management**:
   - Create, edit, and delete tasks.
   - Each task has a title, description, due date, priority level, and status.
   - Users can also add comments on tasks.
   - Users can view and filter tasks by status, priority and due date.

3. **📋 Task Assignment**:
   - Assign tasks to other registered users.
   - User can view tasks assigned to the user on a separate page.

4. **👤 User Profiles**:
   - Profile page where user can upload his profile picture, can view his/her username, and update  first name, last name, about, and email.


6. **✨ Additional Features**:
   - Search functionality to search tasks by title or description.
   - Users can Mark tasks as favorites.
   - Users can add comments to the tasks by allowing users to discuss and provide updates directly within the task.
   - Notifications for task assignments, user will be notified via email whenever a task is assigned to him/her and also whenever a new user signup on platform.
   - Calendar view to visualize tasks based on their due dates.

## Setup Instructions

Follow these steps to set up and run the project locally:

### Prerequisites

- Python 3.10
- MYSQL 8.0

### Direct Access
- I have deployed TaskX on AWS EC2 , you can acces it using the folowing link:
 http://m.spacenex.online:8000

### Local Installation

#### 1. Clone git repository or Download the zip file
```bash
git clone "https://github.com/moazawann/taskx.git"

#change directory(ignore if you downloaded the zip)
cd taskx
```

#### 2. Setup virtual environment
```bash
# Create a virtual environment
python -m venv myenv

# Activate virtual environment
.\venv\Scripts\activate
```


#### 3. Install requirements

```bash
#change directory
cd core
# inside the virtual environment
pip install -r requirements.txt
```

#### 4. Project Structure
```bash
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── tasks/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py 
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py  
│   └── views.py
├── templates/
│   ├── accounts/
│   └── tasks/
└── public/
```


#### 5. Edit project settings
```bash
# open settings file
# core/core/settings.py

# Edit Database configurations with your MySQL configurations.
# create a MYSQL databse
# Search for DATABASES section.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<mysql-database-name',
        'USER': '<mysql-user>',
        'PASSWORD': '<mysql-password>',
        'HOST': '<mysql-host>',
        'PORT': '<mysql-port>',
    }
}
```
#### 6. Run the Server

```bash
#Go to the project directory
cd core

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Run the server
python manage.py runserver
```

#### 7. Run the Email Service
>  **Djano-mailer** - This will be reposnisle for sending the emails to the users without causing delays in the application. 


```bash
# Open up another terminal
# Activate the same virtual environment
.\venv\Scripts\activate

#Go to the project directory
cd core

#run the django-mailer
python manage.py runmailer
```




