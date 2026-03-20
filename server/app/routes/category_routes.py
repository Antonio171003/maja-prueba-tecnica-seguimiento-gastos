from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.category import Category

category_bp = Blueprint("categories", __name__)

@category_bp.route("", methods=["POST"])
def create_category():
    data = request.get_json(silent=True)

    if not data or "name" not in data:
        return jsonify({"error": "Field 'name' is required"}), 400

    if Category.query.filter_by(name=data["name"]).first():
        return jsonify({"error": f"Category '{data['name']}' already exists"}), 400

    category = Category(name=data["name"])
    db.session.add(category)
    db.session.commit()

    return jsonify({"id": category.id, "name": category.name}), 201


@category_bp.route("", methods=["GET"])
def list_categories():
    categories = Category.query.all()

    return jsonify([
        {"id": c.id, "name": c.name}
        for c in categories
    ])

@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({"error": f"Category {category_id} not found"}), 404
    return jsonify(_serialize(category))

@category_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        return jsonify({"error": "Field 'name' is required"}), 400

    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({"error": f"Category {category_id} not found"}), 404

    if Category.query.filter(Category.name == data["name"], Category.id != category_id).first():
        return jsonify({"error": f"Category '{data['name']}' already exists"}), 400

    category.name = data["name"]
    db.session.commit()
    return jsonify(_serialize(category))

@category_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({"error": f"Category {category_id} not found"}), 404
    if category.expenses:
        return jsonify({"error": "Cannot delete category with associated expenses"}), 400

    db.session.delete(category)
    db.session.commit()
    return "", 204

def _serialize(category):
    return {
        "id":         category.id,
        "name":       category.name,
        "created_at": category.created_at.isoformat() if category.created_at else None,
    }