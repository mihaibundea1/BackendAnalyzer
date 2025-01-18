# Folosim o imagine oficială de Python
# FROM python:3.9-slim

# # Setăm directorul de lucru în container
# WORKDIR /app

# # Copiem fișierele aplicației în container
# COPY . /app

# # Creăm și activăm un mediu virtual
# RUN python -m venv venv
# RUN . venv/bin/activate

# # Instalăm dependințele din requirements.txt
# COPY requirements.txt .
# RUN . venv/bin/activate && pip install -r requirements.txt

# # Expunem portul 5000 pentru aplicația Flask
# EXPOSE 5000

# # Comanda de start a aplicației
# CMD ["bash", "-c", ". venv/bin/activate && python main.py"]
