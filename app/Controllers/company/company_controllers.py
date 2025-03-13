from flask import Blueprint, request, jsonify

from app import db

def some_function(company):
    from app.Controllers.company import company_controllers

    



company_bp = Blueprint('company', __name__, url_prefix='/api/v1/company')

from app.Controllers.company import company_controllers
# 1. Create a new company
@company_bp.route('/', methods=['POST'])
def create_company():
    data = request.get_json()
    name = data.get('name')
    location = data.get('location')

    new_company = company_controllers (name=name, location=location)
    db.session.add(new_company)
    db.session.commit()

    return jsonify({'message': 'Company created successfully'}), 201

# 2. Read all companies
@company_bp.route('/', methods=['GET'])
def get_companies():
    companies = company_controllers.query.all()
    return jsonify([company.to_dict() for company in companies]), 200

# 3. Update a company
@company_bp.route('/<int:id>', methods=['PUT'])
def update_company(id):
    data = request.get_json()
    company = company_controllers.query.get(id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    company.name = data.get('name', company.name)
    company.location = data.get('location', company.location)
    db.session.commit()

    return jsonify({'message': 'Company updated successfully'}), 200

# 4. Delete a company
@company_bp.route('/<int:id>', methods=['DELETE'])
def delete_company(id):
    company = company_controllers.query.get(id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    db.session.delete(company)
    db.session.commit()

    return jsonify({'message': 'Company deleted successfully'}), 200
