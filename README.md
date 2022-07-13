Commands:

    py -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    py manage.py runserver


In core /settings.py the stripe is commented out - just put your own details in here (not all of these are connected to the project)

# Stripe Payment
PUBLISHABLE_KEY = ''
SECRET_KEY = ''

# Admin login
1. http://127.0.0.1:8000/admin/
2. username and password = 123

# CARD PAY

REDCOMPRA:      4051 8842 3993 7763

Rut:            11.111.111-1

Clave:          123