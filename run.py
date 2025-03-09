from app import create_app
from flask_cors import CORS
import torch

torch.cuda.empty_cache()

app = create_app()

CORS(app, resources={r"/*": {"origins": "*"}})  # Permite toate originile pentru acest endpoint

if __name__ == "__main__":
    app.run(debug=True)
    