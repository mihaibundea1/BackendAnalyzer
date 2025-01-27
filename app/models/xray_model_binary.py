# app/models/xray_model.py

import torch
import torchvision.transforms as transforms
from torchvision import models
import torch.nn as nn
from PIL import Image

# Image normalization statistics
STATS = ((0.5832, 0.5832, 0.5832), (0.1413, 0.1413, 0.1413))

# Preprocessing transformations
TRANSFORM = transforms.Compose([
    lambda image: image.convert("RGB"),  # Force RGB conversion
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=STATS[0], std=STATS[1]),
])

class XRayClassifier(nn.Module):
    """Custom X-ray classification model based on ResNet18"""
    def __init__(self, num_classes=2):
        super().__init__()
        self.base_model = models.resnet18(weights=models.resnet.ResNet18_Weights.DEFAULT)
        self.features = nn.Sequential(*list(self.base_model.children())[:-1])
        resnet_out_size = self.base_model.fc.in_features
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(resnet_out_size, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

def load_model(model_path, device):
    """Load trained model weights with architecture mismatch handling"""
    model = XRayClassifier(num_classes=2)
    
    # Load state dict with strict=False to ignore missing layers
    state_dict = torch.load(model_path, map_location=device, weights_only=True)
    
    # Filter out unexpected keys (remove conv1.* layers)
    filtered_state_dict = {k: v for k, v in state_dict.items() 
                          if not k.startswith('conv1.')}
    
    model.load_state_dict(filtered_state_dict, strict=False)
    return model.to(device)

def preprocess_image(image_path):
    """Load and transform image for model input"""
    image = Image.open(image_path)
    return TRANSFORM(image).unsqueeze(0)  # Add batch dimension

def predict(model, image_tensor):
    """Run model inference on preprocessed image tensor"""
    model.eval()
    with torch.no_grad():
        outputs = model(image_tensor.to(next(model.parameters()).device))
        return torch.nn.functional.softmax(outputs, dim=1).cpu().numpy().flatten()

def classify_image(model, image_path):
    """End-to-end classification pipeline"""
    image_tensor = preprocess_image(image_path)
    return predict(model, image_tensor)