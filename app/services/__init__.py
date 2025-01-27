from app.services.xray_service_binary import XRayServiceBinary

def create_xray_service(model_path, model_type='binary'):
    """
    Factory method pentru crearea instanței XRayService, în funcție de tipul de model.
    """
    if model_type == 'binary':
        return XRayServiceBinary(model_path=model_path)
    else: 
        return None

