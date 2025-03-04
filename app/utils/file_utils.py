import os
import tempfile

def save_temp_file(file):
    """Salvează un fișier temporar într-un director specificat și returnează calea sa."""
    
    # Calea pentru directorul temporar
    temp_dir = tempfile.gettempdir()
    
    # Creează directorul temporar dacă nu există deja
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Creează un fișier temporar cu un nume unic
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    # Salvează fișierul în directorul temporar
    file.save(temp_file_path)
    
    return temp_file_path
