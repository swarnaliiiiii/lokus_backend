from flask import Blueprint, request, jsonify
from model.input_model import InputService  # Import your existing InputService

# Create the blueprint
budget_bp = Blueprint('budget', __name__, url_prefix='/api/budget')

# Initialize the service
input_service = InputService()

@budget_bp.route('/selections', methods=['POST'])
def create_budget_selection():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['budget', 'duration', 'people_count', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Validate data types
        if not isinstance(data.get('people_count'), int):
            return jsonify({
                'status': 'error',
                'message': 'people_count must be an integer'
            }), 400
        
        # Save the budget selection using your existing service
        result = input_service.save_budget_selection(
            budget=data['budget'],
            duration=data['duration'],
            people_count=data['people_count'],
            type=data['type']
        )
        
        if result['status'] == 'success':
            return jsonify(result), 201
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Invalid request: {str(e)}'
        }), 400

@budget_bp.route('/selections/<selection_id>', methods=['GET'])
def get_budget_selection(selection_id):
    """Get a specific budget selection by ID"""
    try:
        # You'll need to add this method to your InputService
        result = input_service.get_budget_selection(selection_id)
        
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving selection: {str(e)}'
        }), 500

@budget_bp.route('/selections', methods=['GET'])
def get_all_budget_selections():
    """Get all budget selections"""
    try:
        # You'll need to add this method to your InputService
        result = input_service.get_all_budget_selections()
        
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving selections: {str(e)}'
        }), 500

@budget_bp.route('/selections/<selection_id>', methods=['PUT'])
def update_budget_selection(selection_id):
    """Update a budget selection"""
    try:
        data = request.get_json()
        
        # Validate people_count if provided
        if 'people_count' in data and not isinstance(data['people_count'], int):
            return jsonify({
                'status': 'error',
                'message': 'people_count must be an integer'
            }), 400
        
        # You'll need to add this method to your InputService
        result = input_service.update_budget_selection(
            selection_id=selection_id,
            budget=data.get('budget'),
            duration=data.get('duration'),
            people_count=data.get('people_count'),
            type=data.get('type')
        )
        
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 404 if 'not found' in result['message'].lower() else 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error updating selection: {str(e)}'
        }), 400

@budget_bp.route('/selections/<selection_id>', methods=['DELETE'])
def delete_budget_selection(selection_id):
    """Delete a budget selection"""
    try:
        # You'll need to add this method to your InputService
        result = input_service.delete_budget_selection(selection_id)
        
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error deleting selection: {str(e)}'
        }), 500