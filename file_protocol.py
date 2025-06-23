import json
import base64
import os

class FileProtocol:
    def __init__(self):
        self.base_dir = 'files'
        os.makedirs(self.base_dir, exist_ok=True)

    def proses_string(self, string_datamasuk=''):
        string_datamasuk = string_datamasuk.strip()

        if string_datamasuk.upper().startswith("UPLOAD "):
            try:
                cleaned = string_datamasuk[7:]
                if "||" not in cleaned:
                    return json.dumps({'status': 'ERROR', 'data': 'Format upload tidak valid'})

                filename, base64_data = cleaned.split("||", 1)
                filepath = os.path.join(self.base_dir, filename.strip())
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(base64_data.strip()))
                return json.dumps({'status': 'OK', 'data': f'File {filename.strip()} berhasil diupload'})
            except Exception as e:
                return json.dumps({'status': 'ERROR', 'data': str(e)})

        elif string_datamasuk.upper().startswith("DELETE "):
            try:
                filename = string_datamasuk[7:].strip()
                filepath = os.path.join(self.base_dir, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    return json.dumps({'status': 'OK', 'data': f'File {filename} berhasil dihapus'})
                else:
                    return json.dumps({'status': 'ERROR', 'data': 'File tidak ditemukan'})
            except Exception as e:
                return json.dumps({'status': 'ERROR', 'data': str(e)})

        else:
            return json.dumps({'status': 'ERROR', 'data': 'Perintah tidak dikenali'})
