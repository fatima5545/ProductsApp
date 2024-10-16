from flask import Blueprint, jsonify
from flask_restx import Api, Resource, fields
from .models import Product
from .extensions import db

main = Blueprint('main', __name__)
api = Api(main, version='1.0', title='Product API',
          description='A simple Product API',
          doc='/docs')  # URL pour la documentation Swagger

# Définition de la structure du modèle Swagger pour Product
product_model = api.model('Product', {
    'id': fields.Integer(readOnly=True, description='The unique ID of a product'),
    'code': fields.String(required=True, description='Product code'),
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(description='Product description'),
    'image': fields.String(description='Product image URL'),
    'category': fields.String(description='Product category'),
    'price': fields.Float(required=True, description='Product price'),
    'quantity': fields.Integer(required=True, description='Product quantity'),
    'internal_reference': fields.String(description='Internal reference code'),
    'shell_id': fields.Integer(description='Shell ID'),
    'inventory_status': fields.String(required=True, description='Inventory status'),
    'rating': fields.Integer(description='Product rating')
})

# API namespace pour les produits
ns = api.namespace('products', description='Product operations')

@ns.route('/')
class ProductList(Resource):
    @ns.marshal_list_with(product_model)
    def get(self):
        '''Retrieve all products'''
        products = Product.query.all()
        return products

    @ns.expect(product_model)
    @ns.response(201, 'Product successfully created.')
    def post(self):
        '''Create a new product'''
        data = api.payload
        new_product = Product(
            code=data['code'],
            name=data['name'],
            description=data['description'],
            image=data['image'],
            category=data['category'],
            price=data['price'],
            quantity=data['quantity'],
            internal_reference=data['internal_reference'],
            shell_id=data['shell_id'],
            inventory_status=data['inventory_status'],
            rating=data['rating']
        )
        db.session.add(new_product)
        db.session.commit()
        return {"message": "Product created successfully!"}, 201
    
    @ns.response(200, 'All products successfully deleted.')
    def delete(self):
        '''Delete all products'''
        Product.query.delete()
        db.session.commit()
        return {"message": "All products deleted successfully!"}, 200


@ns.route('/<int:id>')
@ns.response(404, 'Product not found')
@ns.param('id', 'The product ID')
class ProductDetail(Resource):
    @ns.marshal_with(product_model)
    def get(self, id):
        '''Fetch a product given its ID'''
        product = Product.query.get_or_404(id)
        return product

    @ns.expect(product_model)
    @ns.response(200, 'Product successfully updated.')
    def put(self, id):
        '''Update a product given its ID'''
        product = Product.query.get_or_404(id)
        data = api.payload

        product.code = data.get('code', product.code)
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.image = data.get('image', product.image)
        product.category = data.get('category', product.category)
        product.price = data.get('price', product.price)
        product.quantity = data.get('quantity', product.quantity)
        product.internal_reference = data.get('internal_reference', product.internal_reference)
        product.shell_id = data.get('shell_id', product.shell_id)
        product.inventory_status = data.get('inventory_status', product.inventory_status)
        product.rating = data.get('rating', product.rating)

        db.session.commit()
        return {"message": "Product updated successfully!"}, 200
    
    @ns.response(200, 'Product successfully deleted.')
    def delete(self, id):
        '''Delete a product given its ID'''
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully!"}, 200
