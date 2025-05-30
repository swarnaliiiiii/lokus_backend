from flask import Flask, jsonify
from flask_cors import CORS
import os
from blueprints.userinput import budget_bp  # Import your blueprint

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.config['DATABASE_PATH'] = os.environ.get('DATABASE_PATH', 'lokus_db')
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(budget_bp)
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Lokus Budget API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'budget_selections': '/api/budget/selections',
                'health_check': '/api/budget/health',
                'api_docs': '/api/docs'
            }
        })
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'message': 'Resource not found',
            'error_code': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'error_code': 500
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'status': 'error',
            'message': 'Bad request',
            'error_code': 400
        }), 400
    
    # API documentation route
    @app.route('/api/docs')
    def api_docs():
        return jsonify({
            'api_documentation': {
                'base_url': '/api/budget',
                'endpoints': [
                    {
                        'method': 'POST',
                        'path': '/selections',
                        'description': 'Create a new budget selection',
                        'body': {
                            'budget': 'string (required)',
                            'duration': 'string (required)',
                            'people_count': 'integer (required)',
                            'type': 'string (required)'
                        }
                    },
                    {
                        'method': 'GET',
                        'path': '/selections',
                        'description': 'Get all budget selections'
                    },
                    {
                        'method': 'GET',
                        'path': '/selections/{id}',
                        'description': 'Get a specific budget selection by ID'
                    },
                    {
                        'method': 'PUT',
                        'path': '/selections/{id}',
                        'description': 'Update a budget selection',
                        'body': {
                            'budget': 'string (optional)',
                            'duration': 'string (optional)',
                            'people_count': 'integer (optional)',
                            'type': 'string (optional)'
                        }
                    },
                    {
                        'method': 'DELETE',
                        'path': '/selections/{id}',
                        'description': 'Delete a budget selection'
                    },
                    {
                        'method': 'GET',
                        'path': '/health',
                        'description': 'Health check endpoint'
                    }
                ]
            }
        })
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    print(f"Starting Lokus Budget API server...")
    print(f"Server running at: http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/api/docs")
    print(f"Health Check: http://{host}:{port}/api/budget/health")
    
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG']
    )