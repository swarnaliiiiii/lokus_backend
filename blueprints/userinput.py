from flask import Flask, request, jsonify, Blueprint
from datetime import datetime
import logging
from model.input_model import InputService

userinput_blueprint = Blueprint('userinput', __name__)

input_service = InputService()

@userinput_blueprint.route('/save_budget_selection', methods=['POST'])
def select_user_input():
    try:
        data = request.get_json()
        
        # Validate request data
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body must contain JSON data'
            }), 400
        
        budget = data.get('budget')
        if not budget:
            return jsonify({
                'error': 'Missing budget field',
                'message': 'Budget field is required'
            }), 400
        
        # Validate budget value
        validation_result = validate_budget_data(budget)
        if not validation_result['valid']:
            return jsonify({
                'error': 'Invalid budget value',
                'message': validation_result['message']
            }), 400
        
        # Process budget selection
        result = input_service.save_budget_selection(budget)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Budget selected successfully',
                'data': {
                    'budget': budget,
                    'timestamp': datetime.utcnow().isoformat(),
                    'budget_id': result['budget_id']
                }
            }), 200
        else:
            return jsonify({
                'error': 'Failed to save budget',
                'message': result['message']
            }), 500

    except Exception as e:
        logging.error(f"Error in select_budget: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500