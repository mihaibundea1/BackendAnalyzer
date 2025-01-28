import torch
from PIL import Image
from torchvision import transforms
from app.models.xray_model_binary import XRayClassifierBinary

STATS = ((0.5832, 0.5832, 0.5832), (0.1413, 0.1413, 0.1413))

class XRayBinaryService:
    def __init__(self):
        self.model = None
        self.transform = transforms.Compose([
            lambda image: image.convert("RGB"),
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=STATS[0], std=STATS[1]),
        ])

    def load_model(self):
        if not self.model:
            self.model = XRayClassifierBinary.load_model()

    def preprocess_image(self, image_path):
        image = Image.open(image_path)
        return self.transform(image).unsqueeze(0)

    def predict_image(self, image_path):
        self.load_model()
        image_tensor = self.preprocess_image(image_path).to(next(self.model.parameters()).device)
        
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probs = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy().flatten()
        
        return {
            'Normal': float(probs[0]),
            'Pneumonia': float(probs[1])
        }

xray_binary_service = XRayBinaryService()