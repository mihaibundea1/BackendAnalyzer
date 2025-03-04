from PIL import Image
import torch
from transformers import BlipForConditionalGeneration, BlipProcessor, TextIteratorStreamer
from threading import Thread
from queue import Empty

class XRayToTextService:
    def __init__(self):
        self.processor = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.loaded = False

    def load_model(self):
        if not self.loaded:
            self.processor = BlipProcessor.from_pretrained("nathansutton/generate-cxr")
            self.model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base").to(self.device)
            self.model.eval()
            self.loaded = True

    def prepare_inputs(self, image_path, indication):
        """Unica definiție corectă - procesează imaginea și creează input-uri"""
        image = Image.open(image_path).convert('RGB')
        image = image.resize((384, 384))  # Redimensionare pentru optimizare
        inputs = self.processor(
            images=image,
            text=f'indication: {indication}',
            return_tensors="pt",
            truncation=True
        ).to(self.device)
        return inputs

    def generate_report(self, image_path, indication):
        self.load_model()
        inputs = self.prepare_inputs(image_path, indication)
        
        with torch.no_grad():
            output = self.model.generate(**inputs, max_length=128)
            
        return self.processor.decode(output[0], skip_special_tokens=True)

    def stream_report(self, image_path, indication):
        self.load_model()
        inputs = self.prepare_inputs(image_path, indication)
        
        streamer = TextIteratorStreamer(
            self.processor.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
            timeout=300
        )
        
        gen_kwargs = {
            **inputs,
            "max_new_tokens": 512,
            "streamer": streamer,
            "num_beams": 1,
            "do_sample": True,
            "temperature": 0.7
        }
        
        generation_thread = Thread(target=self.model.generate, kwargs=gen_kwargs)
        generation_thread.start()
        
        try:
            while True:
                try:
                    for token in streamer:
                        if token:
                            yield token
                    break
                except Empty:
                    if not generation_thread.is_alive():
                        break
                    continue
        finally:
            if generation_thread.is_alive():
                generation_thread.join(timeout=1)

xray_to_text_service = XRayToTextService()