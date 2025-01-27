# app/services/xray_service.py

from app.models.xray_model_binary import load_model, classify_image
import torch

class XRayServiceBinary:
    def __init__(self, model_path):
        self.device = self.get_default_device()
        # Load model and move to device
        self.model = load_model(model_path, self.device)
        
    def classify_image(self, image_path):
        # Use the class-level device when classifying
        return classify_image(self.model, image_path)
    
    def get_default_device(self):
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')