from PIL import Image
import torch
from transformers import BlipForConditionalGeneration, BlipProcessor, TextIteratorStreamer
from threading import Thread
from queue import Empty
import logging

class XRayToTextService:
    def __init__(self):
        self.processor = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.loaded = False

    def load_model(self):
        if not self.loaded:
            # Load the model and processor
            self.processor = BlipProcessor.from_pretrained("nathansutton/generate-cxr")
            self.model = BlipForConditionalGeneration.from_pretrained("nathansutton/generate-cxr").to(self.device)
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

    import logging  # Add this import at the top of the file

    def stream_report(self, image_path, indication):
        self.load_model()
        inputs = self.prepare_inputs(image_path, indication)
        streamer = TextIteratorStreamer(
            self.processor.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
            timeout=1  # Check frequently for new tokens
        )
        gen_kwargs = {
            **inputs,
            "max_new_tokens": 512,
            "streamer": streamer,
            "num_beams": 1,
            "do_sample": True,
            "temperature": 0.7
        }
        
        # Optionally, create a cancellation event:
        # self.cancel_event = threading.Event()
        # And pass it to a wrapper that checks for cancellation
        
        generation_thread = Thread(target=self.model.generate, kwargs=gen_kwargs)
        generation_thread.daemon = True  # Mark thread as daemon so it won't block exit
        generation_thread.start()
        
        try:
            while generation_thread.is_alive():
                try:
                    token = streamer.__next__()
                    yield token
                except StopIteration:
                    break
                except Empty:
                    continue
        except GeneratorExit:
            logging.info("Conexiunea client închisă, oprire generare...")
            raise
        finally:
            if generation_thread.is_alive():
                generation_thread.join(timeout=2)
            if generation_thread.is_alive():
                logging.warning("Thread-ul de generare nu s-a închis corect")

                        

xray_to_text_service = XRayToTextService()