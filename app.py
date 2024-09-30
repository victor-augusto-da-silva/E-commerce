from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user,LoginManager, login_required,logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecomerce.db'

#Controla os acessos
login_manager =  LoginManager()

# Inicia conexão
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)



# Modelagem de usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

# Modelagem de produto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


#Autenticação para rotas protegidas
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Rota de login
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and data.get("password") == user.password:
        login_user(user)
        return jsonify({"message": "Logged in successfully"})
    return jsonify({"message": "Unauthorized: Invalid Credentials"}), 401

@app.route('/logout',methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message":"Logout successfully"})


# Rota de adicionar produto
@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})
    return jsonify({"message": "Invalid product data"}), 400

# Rota de deletar produto
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Product not found"}), 404

# Rota para detalhes do produto
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
    return jsonify({"message": "Product not found"}), 404

# Rota de atualizar produto
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.json
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

# Rota para listar todos os produtos
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{
        "id": product.id,
        "name": product.name,
        "price": product.price
    } for product in products]
    return jsonify(product_list)

# Rota raiz
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True)
