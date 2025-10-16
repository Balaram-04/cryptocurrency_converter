# cryptocurrency_converter
web: gunicorn crypto_converter.wsgi --log-file -


python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py collectstatic --noinput
python manage.py runserver
