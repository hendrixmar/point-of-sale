import json

import flask
from flask import request, redirect, url_for, jsonify

from app import app
from app import db
from app.models import *
from infraestructure.view_modifiers import response



@app.route('/billing')
@response(template_file='/ventas/ventas.html')
def make_sale():
    productos = Products.query.all()

    return {'products': productos}







@app.route('/make_sale', methods=['POST', 'GET'])
def sales():
    if request.method == "POST":
        content = request.get_json()
        print(content)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}




@app.route('/product/get/<int:product_id>',methods=['GET'])
def get_product_by_id(product_id):
    if request.method == "GET":
        product = Products.query.filter_by(id=product_id).all()



        if product == []:
            return json.dumps({'error':True}), 500, {'ContentType':'application/json'}

        else:
            product = product[0]
            prices = [[i.price, i.quantity] for i in product.prices]

            return jsonify(name=product.name,
                           quantity=product.quantity,
                           description=product.description,
                           prices=prices,
                           id=product_id)