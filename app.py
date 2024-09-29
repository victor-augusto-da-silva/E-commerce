#importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecomerce.db'



#inicia conexão 
db=SQLAlchemy(app)

#modelagem
class Product(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False )
    description = db.Column(db.Text,nullable=True)

#rota de adicionar produto
@app.route('/api/products/add', methods=["POST"])
def add_product(): 
    data = request.json
    #data[""] campo obrigatorio
    #data.get("") campo opicional
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"],price=data["price"],description=data.get("description",""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message" : "Product added successully"})
    return jsonify({"message:": "Invalid product data"}),400


#rota de deletar
@app.route('/api/products/delete/<int:product_id>',methods=["DELETE"])
def delete_product(product_id): 
    #Recupera se valido
    product = Product.query.get(product_id)
    if product: 
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successully"})
    return jsonify({"message": "Product not found"}),404


#rota retorna os detalhes do produto
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_products_details(product_id):
        product = Product.query.get(product_id)
        if product:
             return jsonify({
                  "id": product.id,
                  "name": product.name,
                  "price": product.price,
                  "description": product.description
             })
        return jsonify({"message": "Product not fount"}),404

#rota de atualizar
@app.route('/api/products/update/<int:product_id>',methods=["PUT"])
def update_product(product_id): 
    #atualiza se valido
    product = Product.query.get(product_id)
    if product: 
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successully"})
    return jsonify({"message": "Product not found"}),404


#Rota raíz
@app.route('/')
def hello_world(): return 'Hello World'

if __name__ == "__main__": app.run(debug=True)
