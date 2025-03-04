from .xray_service_binary import xray_binary_service
from .xray_service_multi import xray_multi_service
from .xray_to_text import xray_to_text_service

__all__ = ['xray_binary_service', 'xray_multi_service']

def register_services(app):
    # Initialize services
    xray_binary_service.load_model()
    xray_multi_service.load_model()
    xray_to_text_service.load_model()