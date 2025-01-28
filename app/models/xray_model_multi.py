# models/xray_model_multi.py
import torch
import torch.nn as nn
import torchvision

class DenseNet121Multi(nn.Module):
    """Model modificat pentru clasificare multi-class"""
    def __init__(self, out_size=14):
        super().__init__()
        self.densenet121 = torchvision.models.densenet121(pretrained=True)
        num_ftrs = self.densenet121.classifier.in_features
        self.densenet121.classifier = nn.Sequential(
            nn.Linear(num_ftrs, out_size),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.densenet121(x)

    @classmethod
    def load_model(cls, checkpoint_path='models/pytorch_models/chest_xray_multi.pth.tar'):
        model = cls().cuda()
        checkpoint = torch.load(checkpoint_path)
        state_dict = {k.replace('module.', ''): v for k, v in checkpoint['state_dict'].items()}
        model.load_state_dict(state_dict, strict=False)
        model.eval()
        return model