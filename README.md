
# invoicing

This is a small microservice for invoicing. An invoice represents an amount of money to be paid. The amount can be paid in one or more payments. A payment can be for part of the invoice amount.

You can see the requirements of the coding exercise in TASK.md.

## How to install and run.
The folowing instructions will work for Linux and Mac OS X. Make sure you have python 3 installed before continuing.

Go to the root of the directory (the same location as this file) and run the following:

1. Create a virtual environment:

        python3 -m venv env

1. Activate the virtual environment:

        source env/bin/activate

1. Install the python requirements:

        pip install -r requirements.txt

1. Create the database

        alembic upgrade head

1. Run the server

        FLASK_APP=invoicing FLASK_DEBUG=1 flask run

## Tests
There are some automated tests. To run them, go to the root of the directory and run:

    pytest

## Routes
The following routes exist:

* `GET /invoices/`: List all invoices.
* `GET /invoices/<invoice_id>/`: View a particular invoice.
* `POST /invoices/`: Create an invoice.
* `POST /invoices/<invoice_id>/pay/`: Pay for an invoice.
