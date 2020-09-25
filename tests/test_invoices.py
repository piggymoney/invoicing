
from decimal import Decimal

from invoicing import db
from invoicing.models import Invoice

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"


def test_list_invoices(client):
    with db.connection() as DB:
        invoice = Invoice(amount=5, description='Test invoice')
        DB.add(invoice)

    response = client.get('/invoices/')
    data = response.json
    for n in range(len(data)):
        data[n]['amount'] = Decimal(data[n]['amount'])
        data[n]['amount_remaining'] = Decimal(data[n]['amount_remaining'])

    invoice_details = invoice.to_json()
    invoice_details['created_at'] = invoice_details['created_at'].strftime(DATE_FORMAT)  # noqa
    invoice_details['updated_at'] = invoice_details['updated_at'].strftime(DATE_FORMAT)  # noqa

    assert data == [invoice_details]


def test_get_invoice(client):
    with db.connection() as DB:
        invoice = Invoice(amount=5, description='Test invoice')
        DB.add(invoice)

    response = client.get('/invoices/{0}/'.format(invoice.id))
    data = response.json
    data['amount'] = Decimal(data['amount'])
    data['amount_remaining'] = Decimal(data['amount_remaining'])

    invoice_details = invoice.to_json()
    invoice_details['created_at'] = invoice_details['created_at'].strftime(DATE_FORMAT)  # noqa
    invoice_details['updated_at'] = invoice_details['updated_at'].strftime(DATE_FORMAT)  # noqa

    assert data == invoice_details


def test_pay_invoice(client):
    with db.connection() as DB:
        invoice = Invoice(amount=5, description='Test invoice')
        DB.add(invoice)

    request_data = {'amount': 5}

    response = client.post('/invoices/{0}/pay/'.format(invoice.id),
                           json=request_data)
    data = response.json

    print(data)

    assert data['amount_remaining'] == 0
    assert data['status'] == 'Paid'


# def test_get_balance(client):
#     with db.connection() as DB:
#         invoice = Invoice(amount=5, description='Test invoice')
#         DB.add(invoice)

#     request_data = {'amount': 5}

#     client.post('/invoices/{0}/pay/'.format(invoice.id),
#                 json=request_data)

#     response = client.get('/invoices/balance/')
#     data = response.json

#     assert data['balance'] == 5
