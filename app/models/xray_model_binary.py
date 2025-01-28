import torch
import torch.nn as nn
from torchvision import models

class XRayClassifierBinary(nn.Module):
    """Custom X-ray binary classification model based on ResNet18"""
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

    @classmethod
    def load_model(cls, model_path='app/models/pytorch_models/chest_xray_binary.pth'):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = cls().to(device)
        
        state_dict = torch.load(model_path, map_location=device, weights_only=True)
        filtered_state_dict = {k: v for k, v in state_dict.items() 
                              if not k.startswith('conv1.')}
        
        model.load_state_dict(filtered_state_dict, strict=False)
        model.eval()
        return model