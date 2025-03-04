from app import create_app
import torch

torch.cuda.empty_cache()

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
    