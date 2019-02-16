
from __future__ import absolute_import

from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request

from . import db
from .models import Invoice, InvoicePayment

blueprint = Blueprint('invoices', __name__)


@blueprint.route('/', methods=['POST'])
def create_invoice():
    body = request.json

    try:
        description = body['description']
    except KeyError:
        return jsonify({'error': "A description is required."}), 400

    if not description:
        return jsonify({'error': "Description cannot be empty."}), 400

    try:
        a = body['amount']
    except KeyError:
        return jsonify({'error': "An amount is required."}), 400

    try:
        amount = Decimal(a)
    except InvalidOperation:
        return jsonify({'error': "Amount must be a valid decimal."}), 400

    if amount.as_tuple().exponent < -2:
        return jsonify({'error': "Amount cannot have more than two decimal "
                                 "places"}), 400

    invoice = Invoice(amount=amount, description=description)

    with db.connection() as DB:
        DB.add(invoice)

    return jsonify(invoice.to_json()), 201


@blueprint.route('/<int:invoice_id>/', methods=['GET'])
def retrieve_invoice(invoice_id):
    with db.connection() as DB:
        invoice = DB.query(Invoice).get(invoice_id)

    if invoice is None:
        return jsonify({'error': 'Not found.'}), 404

    return jsonify(invoice.to_json())


@blueprint.route('/', methods=['GET'])
def list_invoices():
    with db.connection() as DB:
        invoices = DB.query(Invoice)

    return jsonify([i.to_json() for i in invoices])


@blueprint.route('/<int:invoice_id>/pay/', methods=['POST'])
def pay_invoice(invoice_id):
    body = request.json

    try:
        a = body['amount']
    except KeyError:
        return jsonify({'error': "An amount is required."}), 400

    try:
        amount = float(a)
    except ValueError:
        return jsonify({'error': "Amount must be a valid number."}), 400

    with db.connection() as DB:
        invoice = DB.query(Invoice).get(invoice_id)

        if invoice is None:
            return jsonify({'error': 'Not found.'}), 404

        if invoice.status == Invoice.PAID:
            return jsonify({'error': "Cannot pay any invoice which is already "
                                     "paid"}), 400

        other_payments = DB.query(InvoicePayment) \
                           .filter(InvoicePayment.invoice_id == invoice_id)

        amount_remaining = invoice.amount - sum(p.amount
                                                for p in other_payments)

        if amount > amount_remaining:
            return jsonify({'error': "Cannot pay more than the remaining "
                                     "amount."}), 400

        payment = InvoicePayment(invoice_id=invoice_id, amount=amount)
        DB.add(payment)

        if amount_remaining == amount:
            invoice.status = Invoice.PAID

    return jsonify(invoice.to_json())


@blueprint.route('/balance', methods=['GET'])
def balance():
    balance = Decimal('0')

    with db.connection() as DB:
        invoices = DB.query(Invoice)

        for invoice in invoices:
            for payment in invoice.payments:
                if payment.amount == invoice.amount:
                    balance += payment.amount
                else:
                    balance -= payment.amount

    return jsonify({'balance': balance})
