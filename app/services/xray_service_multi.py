from PIL import Image
import torch
from torchvision import transforms
from app.models.xray_model_multi import DenseNet121Multi

CLASS_NAMES = ['Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltration', 'Mass', 
              'Nodule', 'Pneumonia', 'Pneumothorax', 'Consolidation', 'Edema', 
              'Emphysema', 'Fibrosis', 'Pleural_Thickening', 'Hernia']

class XRayMultiService:
    def __init__(self):
        self.model = None
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.TenCrop(224),
            transforms.Lambda(lambda crops: torch.stack([
                transforms.ToTensor()(crop) for crop in crops
            ])),
            transforms.Lambda(lambda crops: torch.stack([
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(crop)
                for crop in crops
            ]))
        ])

    def load_model(self):
        if not self.model:
            self.model = DenseNet121Multi.load_model()

    def predict_image(self, image_path):
        self.load_model()
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0)
        input_var = input_tensor.view(-1, 3, 224, 224).cuda()
        
        with torch.no_grad():
            output = self.model(input_var)
            output_mean = output.view(1, 10, -1).mean(1)
        
        probs = output_mean.squeeze().cpu().numpy()
        return {CLASS_NAMES[i]: float(probs[i]) for i in range(len(CLASS_NAMES))}

xray_multi_service = XRayMultiService()