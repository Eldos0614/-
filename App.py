from flask import Flask, request, jsonify

app = Flask(__name__)

# Уақытша деректер қоры (memory)
products = [
    {"id": 1, "name": "Ноутбук", "quantity": 10, "price": 250000},
    {"id": 2, "name": "Тінтуір", "quantity": 50, "price": 5000},
    {"id": 3, "name": "Пернетақта", "quantity": 30, "price": 12000},
]


# Басты бет
@app.route("/")
def home():
    return jsonify({
        "message": "Қойма басқару жүйесіне қош келдіңіз!"
    })


# Барлық тауарларды шығару
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


# Бір тауарды ID бойынша шығару
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)
    return jsonify({"error": "Тауар табылмады"}), 404


# Жаңа тауар қосу
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Мәлімет жіберілмеді"}), 400

    required_fields = ["name", "quantity", "price"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} өрісі міндетті"}), 400

    new_product = {
        "id": products[-1]["id"] + 1 if products else 1,
        "name": data["name"],
        "quantity": data["quantity"],
        "price": data["price"]
    }

    products.append(new_product)
    return jsonify({
        "message": "Тауар сәтті қосылды",
        "product": new_product
    }), 201


# Тауарды жаңарту
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()

    for product in products:
        if product["id"] == product_id:
            product["name"] = data.get("name", product["name"])
            product["quantity"] = data.get("quantity", product["quantity"])
            product["price"] = data.get("price", product["price"])

            return jsonify({
                "message": "Тауар сәтті жаңартылды",
                "product": product
            })

    return jsonify({"error": "Тауар табылмады"}), 404


# Тауарды өшіру
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return jsonify({"message": "Тауар сәтті өшірілді"})
    return jsonify({"error": "Тауар табылмады"}), 404


if __name__ == "__main__":
    app.run(debug=True)
