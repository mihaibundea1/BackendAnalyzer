from app.repositories.investigation_repository import InvestigationRepository
from werkzeug.utils import secure_filename
import os
from ..utils.blackblaze import upload_file
from flask import current_app
import uuid

class InvestigationService:
    @staticmethod
    def get_all_investigations():
        return InvestigationRepository.get_all()

    @staticmethod
    def get_investigation_details(investigation_id):
        return InvestigationRepository.get_by_id(investigation_id)

    @staticmethod
    def create_investigation(files, form):
        file = files.get('file')
        if file:
            file_name = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            bucket_name = current_app.config["BUCKET_NAME"]

            local_path = os.path.join('temp_uploads', file_name)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            file.save(local_path)

            try:
                upload_file(b2_api=current_app.b2_api, 
                            bucket_name=bucket_name,
                            local_file_path=local_path,
                            file_name_in_bucket=file_name)
                
                file_url = f"https://f000.backblazeb2.com/file/{bucket_name}/{file_name}"

                # Creează o copie a formului pentru a adăuga un nou câmp
                form_copy = form.to_dict()  # Creează o copie dict a formului
                form_copy['image_path'] = file_url  # Adaugă URL-ul fișierului

                new_investigation = InvestigationRepository.create(form_copy)
                
                os.remove(local_path)

                return new_investigation
            except Exception as e:
                print(f"Error uploading file: {str(e)}")
                return None
        else:
            # Dacă nu există fișier, doar creează investigația fără fișier
            return InvestigationRepository.create(form)

    @staticmethod
    def delete_investigation(investigation_id):
        return InvestigationRepository.delete(investigation_id)
