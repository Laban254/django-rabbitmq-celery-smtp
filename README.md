# Django Project Deployment with Gunicorn, Nginx, RabbitMQ, Celery, and ngrok

This README outlines the steps to deploy a Django project using Gunicorn, Nginx, RabbitMQ, Celery, and ngrok.





```gunicorn --bind 0.0.0.0:8003  messaging_system.wsgi```

   ``` celery -A messaging_system worker -l info```

```cat /var/log/messaging_system.log```










## Prerequisites

- Python 3.x
- Django
- Gunicorn
- Nginx
- RabbitMQ
- Celery
- ngrok
- Virtual environment 

## Step 1: Setting Up Your Django Project

1. Navigate to your Django project directory:

    ```bash
    cd /path/to/your/django/project
    ```

2. Ensure your Django settings are configured for static files:

    ```python
    # settings.py
    import os
    from decouple import config

    SECRET_KEY = config('SECRET_KEY')

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

    # Celery configuration
    CELERY_BROKER_URL = 'amqp://localhost'
    CELERY_RESULT_BACKEND = 'django-db'

    ```

3. Collect static files:

    ```bash
    python manage.py collectstatic
    ```

## Step 2: Setting Up RabbitMQ and Celery

1. **Install RabbitMQ:**

    ```bash
    sudo apt-get update
    sudo apt-get install rabbitmq-server
    sudo systemctl enable rabbitmq-server
    sudo systemctl start rabbitmq-server
    ```

2. **Install Celery:**

    ```bash
    pip install celery
    ```

3. **Create Celery configuration:**

    ```python
    # project/celery.py
    from __future__ import absolute_import, unicode_literals
    import os
    from celery import Celery

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

    app = Celery('project')

    app.config_from_object('django.conf:settings', namespace='CELERY')

    app.autodiscover_tasks()
    ```

    ```python
    # project/__init__.py
    from __future__ import absolute_import, unicode_literals

    # This will make sure the app is always imported when Django starts so that shared_task will use this app.
    from .celery import app as celery_app

    __all__ = ('celery_app',)
    ```

5. **creat a task:**
5. **Start Celery worker:**

    ```bash
    celery -A messaging_system worker --loglevel=info
    ```

## Step 3: Running Gunicorn

1. Activate your virtual environment (if using):

    ```bash
    source /path/to/your/virtualenv/bin/activate
    ```

2. Start Gunicorn:

    ```bash
    gunicorn --bind 0.0.0.0:8002 messaging_system.wsgi
    ```

## Step 4: Configuring Nginx

1. Create an Nginx configuration file for your project:

    ```bash
    sudo nano /etc/nginx/sites-available/default
    ```

2. Add the following configuration:

    ```nginx
    server {
        listen 80 default_server;
        listen [::]:80 default_server;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /path/to/your/django/project/staticfiles/;
        }

        location /media/ {
            alias /path/to/your/django/project/media/;
        }

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;
    }
    ```

3. Enable the Nginx configuration:

    ```bash
    sudo ln -s /etc/nginx/sites-available/django_project /etc/nginx/sites-enabled/
    ```

4. Test the Nginx configuration:

    ```bash
    sudo nginx -t
    ```

5. Restart Nginx:

    ```bash
    sudo systemctl restart nginx
    ```

## Step 5: Setting Up ngrok

1. Sign up for an ngrok account: [ngrok signup page](https://dashboard.ngrok.com/signup).

2. Get your authentication token: [ngrok authtoken page](https://dashboard.ngrok.com/get-started/your-authtoken).

3. Authenticate ngrok:

    ```bash
    ngrok authtoken YOUR_AUTH_TOKEN
    ```

    Replace `YOUR_AUTH_TOKEN` with the token you copied.

4. Start ngrok to expose your local server:

    ```bash
    ngrok http 80
    ```

    This will provide you with a public URL (e.g., `http://<random-string>.ngrok.io`).

## Summary

By following these steps, you will have your Django application running with Gunicorn, served by Nginx, using RabbitMQ and Celery for background tasks, and exposed to the internet using ngrok. You can access your application using the public URL provided by ngrok.

## Troubleshooting

- Ensure all services (Gunicorn, Nginx, RabbitMQ, Celery, and ngrok) are running correctly.
- Check log files for errors:
    - Gunicorn logs
    - Nginx logs (`/var/log/nginx/access.log` and `/var/log/nginx/error.log`)
    - RabbitMQ logs
    - Celery logs
- Verify your environment variables, especially `SECRET_KEY`.

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Celery Documentation](https://docs.celeryproject.org/)
- [ngrok Documentation](https://ngrok.com/docs)
