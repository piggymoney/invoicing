
from __future__ import absolute_import

from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from sqlalchemy.orm.exc import NoResultFound

from .db import Session
from .models import Invoice

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

    s = Session()

    s.add(invoice)
    s.commit()

    return jsonify(invoice.to_json()), 201


@blueprint.route('/<int:invoice_id>/', methods=['GET'])
def retrieve_invoice(invoice_id):
    s = Session()

    invoice = s.query(Invoice).get(invoice_id)

    if invoice is None:
        return jsonify({'error': 'Not found.'}), 404

    return jsonify(invoice.to_json())


@blueprint.route('/', methods=['GET'])
def list_invoices():
    s = Session()

    invoices = s.query(Invoice)

    return jsonify([i.to_json() for i in invoices])
