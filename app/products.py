from flask import *
import json
from app import app
from app import db
from app.models import *
from infraestructure.view_modifiers import response


@app.route('/products/show')
@response(template_file='productos/productos.html')
def show_all_products():
    productos = Products.query.all()

    return {'products': productos}


@app.route('/products/json')
def json_products():
    productos = Products.query.all()
    data_json = {}

    for product in productos:

        temp = []
        for i, prices in enumerate(product.prices):
            temp.append([prices.price, prices.quantity])

        data_json[product.id] = {}
        data_json[product.id]['prices'] = temp
        data_json[product.id]['name'] = product.name
        data_json[product.id]['quantity'] = product.quantity


    return data_json


@app.route('/products/delete/<int:product_id>')
@response(template_file='productos/productos.html')
def delete_product(product_id):
    Products.query.filter(Products.id == product_id).delete()
    Prices.query.filter(Prices.product_id == product_id).delete()
    db.session.commit()
    return redirect(url_for('show_all_products'))


@app.route('/products/edit/<int:product_id>', methods=['POST', 'GET'])
def edit_product(product_id):
    product = Products.query.filter_by(id=product_id).first()
    if request.method == "POST":
        content = request.get_json()
        print(content)

        product.name = content['name']

        product.quantity = int(content['total_quantity'])
        product.description = content['description']
        product.cost_price = content['cost_price']
        print(content)

        i = 0
        while f'quantity_{i}' in content or \
                f'price_{i}' in content:

            quantity = int(content[f'quantity_{i}'])
            price = float(content[f'price_{i}'])

            product.prices[i].price = price
            product.prices[i].quantity = quantity

            i += 1

        db.session.add(product)
        db.session.commit()

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


    else:

        return render_template('productos/editar_producto.html', product=product)


@app.route('/products/add/', methods=['POST', 'GET'])
def add_product():

    if request.method == "POST":
        content = request.get_json()
        print(content)
        new_product = Products(name=content['name'],
                               id=content['id'],
                               cost_price=float(content['cost_price']),
                               quantity=int(content['total_quantity']),
                               description=content['description'])

        i = 0
        while f'quantity_{i}' in content  or \
                f'price_{i}' in content:


            quantity = int(content[f'quantity_{i}'])
            price = float(content[f'price_{i}'])

            temp = Prices(price=price, quantity=quantity)

            new_product.prices.append(temp)
            i += 1

        db.session.add(new_product)
        db.session.commit()
        db.session.close()

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    else:
        return render_template('productos/nuevo_producto.html')
