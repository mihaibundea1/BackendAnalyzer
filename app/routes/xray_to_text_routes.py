from flask import Blueprint, request, Response, stream_with_context, jsonify  # Corectat
from app.services.xray_to_text import xray_to_text_service
from app.utils.file_utils import save_temp_file
import os
import logging
from queue import Empty

xray_to_text_bp = Blueprint('xray_to_text', __name__)

@xray_to_text_bp.route('/stream-report', methods=['POST'])
def stream_report():
    if 'file' not in request.files:
        return {'error': 'No file uploaded'}, 400
    
    file = request.files['file']
    indication = request.form.get('indication', '')
    temp_path = save_temp_file(file)
    
    try:
        def generate_stream():
            try:
                # 1. Stream the actual content
                for token in xray_to_text_service.stream_report(temp_path, indication):
                    yield f"data: {token}\n\n"
                
                # 2. Yield the end event ONLY if the loop completes normally
                yield "event: end\ndata: stream_complete\n\n"
                
            except Exception as e:
                logging.error(f"Stream error: {str(e)}")
                # Use a try-except yield here if needed, but avoid finally yields
                yield f"data: [ERROR] {str(e)}\n\n"
            finally:
                # 3. Cleanup happens here without yielding
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        return Response(
            stream_with_context(generate_stream()),
            mimetype='text/event-stream',
            headers={'X-Accel-Buffering': 'no'}
        )
    
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return {'error': str(e)}, 500

@xray_to_text_bp.route('/generate-report', methods=['POST'])
def generate_report_stream():
    if 'file' not in request.files:
        return {'error': 'No file uploaded'}, 400
    
    file = request.files['file']
    indication = request.form.get('indication', '')
    temp_path = save_temp_file(file)
    
    try:
        report = xray_to_text_service.generate_report(temp_path, indication)
        os.remove(temp_path)
        return jsonify({"report": report})  # Acum funcționează corect
    
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return {'error': str(e)}, 500