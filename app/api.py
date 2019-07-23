from flask import (
    Blueprint, g, redirect, request, url_for, current_app, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from copy import deepcopy

def get_stripe():
    if 'stripe' not in g:
        import stripe
        stripe.api_key = current_app.config['stripe']['secret']
        g.stripe = stripe
    return g.stripe

bp = Blueprint('api_v0', __name__, url_prefix='/api/v0')

@bp.route('/tickets/purchase', methods=('POST',))
def ticket_purchase():
    body = request.get_json()

    status = {'success': 'false'}

    # create an order, fill with metadata, then pay with the stripe token acquired from the body
    # fill the rest of the fields with metadata from the body

    # simple sanity check for the form
    if not 'ticket_id' in body:
        status['error'] = 'No ticket ID specified!'
        return jsonify(status), 400
    if not 'stripe_token' in body:
        status['error'] = 'No stripe token included!'
        return jsonify(status), 400

    # retrieve the SKU of the ticket token
    db = get_db()
    c  = db.cursor()
    c.execute('SELECT sku FROM Tickets WHERE key=?', (body['ticket_id'],))
    ticket_sku = c.fetchone()['sku']


    # get the stripe payment token
    payment_token = body['stripe_token']['id']


    # create the metadata for the stripe order
    metadata = deepcopy(body)
    del metadata['stripe_token']
    
    # initialize stripe
    stripe = get_stripe()

    # create the order...
    order = None
    try:
        order = stripe.Order.create(
            items=[{
                'type': 'sku',
                'parent': ticket_sku
            }],
            currency='gbp',
            metadata=metadata,
            email=metadata['email']
        )
    except stripe.error.CardError:
        # gracefully handle the error otherwise
        ebody = e.json_body
        err  = ebody.get('error', {})
        err_type = err.get('type')
        if err_type == 'sku_inactive' or err_type == 'product_inactive':
            status['error'] = 'Sorry! Sales for this ticket have closed.'
        elif err_type == 'out_of_inventory':
            status['error'] = 'Sorry! This ticket has sold out.'
        else:
            status['error'] = err_type + ': ' + err.get('message')


        return jsonify(status), 500

    # ... and pay the order with the token we received
    try:
        order = stripe.Order.pay(
            order['id'],
            source=payment_token
        )
    except stripe.error.CardError:
        ebody = e.json_body
        err  = ebody.get('error', {})
        status['error'] = err.get('message')
        return jsonify(status), 500
    

    # Success!
    
    status['order_id'] = order['id']
    status['success']  = True

    return jsonify(status), 200


@bp.route('/tickets/stripe/token')
def get_stripe_token():
    token = current_app.config['stripe']['token']

    return jsonify({'token': token})
