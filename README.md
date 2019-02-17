
# invoicing

This is a small microservice for invoicing.

## How to run
Go to the root of the directory (the same location as this file) and run:

    FLASK_APP=invoicing FLASK_DEBUG=1 flask run

## Tests
There are some automated tests. To run them, go to the root of the directory and run:

    pytest

## Routes
The following routes exist:

* `GET /invoices/`: List all invoices.
* `GET /invoices/<invoice_id/`: View a particular invoice.
* `POST /invoices/`: Create an invoice.
* `POST /invoices/<invoice_id/pay/`: Pay for an invoice.
* `GET /invoices/balance/`: Display the current balance of invoice payments.
