"""
Vector Database Route Handlers
=============================

Individual route handlers for vector database operations.
V2 Compliance: < 300 lines, single responsibility, route handling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from flask import request, jsonify
from .models import VectorDatabaseModels
from .utils import VectorDatabaseUtils
from .middleware import VectorDatabaseMiddleware


class SearchHandler:
    """Search operation handler."""
    
    @staticmethod
    @VectorDatabaseMiddleware.error_handler
    @VectorDatabaseMiddleware.json_required
    @VectorDatabaseMiddleware.validate_request(VectorDatabaseModels.validate_search_request)
    def handle_search():
        """Handle search requests."""
        data = request.get_json()
        search_request = VectorDatabaseModels.create_search_request(data)
        
        results = VectorDatabaseUtils.simulate_vector_search(search_request)
        
        return jsonify({
            'success': True,
            'results': [result.__dict__ for result in results],
            'query': search_request.query,
            'collection': search_request.collection,
            'search_type': search_request.search_type,
            'total_results': len(results),
            'execution_time': 245
        })


class DocumentHandler:
    """Document operation handler."""
    
    @staticmethod
    @VectorDatabaseMiddleware.error_handler
    @VectorDatabaseMiddleware.validate_pagination
    def handle_get_documents():
        """Handle get documents requests."""
        pagination_request = VectorDatabaseModels.create_pagination_request(request.args)
        result = VectorDatabaseUtils.simulate_get_documents(pagination_request)
        
        return jsonify({
            'success': True,
            'documents': result['documents'],
            'pagination': result['pagination'],
            'total_documents': result['total']
        })
    
    @staticmethod
    @VectorDatabaseMiddleware.error_handler
    @VectorDatabaseMiddleware.json_required
    @VectorDatabaseMiddleware.validate_request(VectorDatabaseModels.validate_document_request)
    def handle_add_document():
        """Handle add document requests."""
        data = request.get_json()
        document_request = VectorDatabaseModels.create_document_request(data)
        
        document = VectorDatabaseUtils.simulate_add_document(document_request)
        
        return jsonify({
            'success': True,
            'document': document.__dict__,
            'message': 'Document added successfully'
        })
    
    @staticmethod
    @VectorDatabaseMiddleware.error_handler
    def handle_get_document(document_id: str):
        """Handle get document requests."""
        document = VectorDatabaseUtils.simulate_get_document(document_id)
        
        if not document:
            return jsonify({
                'success': False,
                'error': 'Document not found'
            }), 404
        
        return jsonify({
            'success': True,
            'document': document.__dict__
        })
    
    @staticmethod
    @VectorDatabaseMiddleware.error_handler
    @VectorDatabaseMiddleware.json_required
    def handle_update_document(document_id: str):
        """Handle update document requests."""
        data = request.get_json()
        document = VectorDatabaseUtils.simulate_update_document(document_id, data)
        
        if not document:
            return jsonify({
                'success': False,
                'error': 'Document not found'
            }), 404
        
        return jsonify({
            'success': True,
            'document': document.__dict__,
            'message': 'Document updated successfully'
        })
    
    @staticmethod
    @VectorDatabaseMiddleware.error_handler
    def handle_delete_document(document_id: str):
        """Handle delete document requests."""
        success = VectorDatabaseUtils.simulate_delete_document(document_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Document not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Document deleted successfully'
        })


class AnalyticsHandler:
    """Analytics operation handler."""
    
    @staticmethod
    @VectorDatabaseMiddleware.error_handler
    def handle_get_analytics():
        """Handle get analytics requests."""
        time_range = request.args.get('time_range', '24h')
        analytics = VectorDatabaseUtils.simulate_get_analytics(time_range)
        
        return jsonify({
            'success': True,
            'analytics': analytics.__dict__
        })


class CollectionHandler:
    """Collection operation handler."""
    
    @staticmethod
    @VectorDatabaseMiddleware.error_handler
    def handle_get_collections():
        """Handle get collections requests."""
        collections = VectorDatabaseUtils.simulate_get_collections()
        
        return jsonify({
            'success': True,
            'collections': [collection.__dict__ for collection in collections]
        })


class ExportHandler:
    """Export operation handler."""
    
    @staticmethod
    @VectorDatabaseMiddleware.error_handler
    @VectorDatabaseMiddleware.json_required
    def handle_export_data():
        """Handle export data requests."""
        data = request.get_json()
        export_request = VectorDatabaseModels.create_export_request(data)
        export_data = VectorDatabaseUtils.simulate_export_data(export_request)
        
        return jsonify({
            'success': True,
            'export_data': export_data.__dict__
        })
