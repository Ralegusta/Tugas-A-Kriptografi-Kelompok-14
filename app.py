import os
import io
import base64
from flask import Flask, render_template, request, send_file, flash
from werkzeug.utils import secure_filename
from ciphers import shift_cipher, substitution_cipher, affine_cipher, vigenere_cipher, hill_cipher, permutation_cipher

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Configuration
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

CIPHER_MAP = {
    'shift': shift_cipher,
    'substitution': substitution_cipher,
    'affine': affine_cipher,
    'vigenere': vigenere_cipher,
    'hill': hill_cipher,
    'permutation': permutation_cipher,
}

def process_file_content(data, cipher_module, action, key):
    """Process file content for encryption/decryption"""
    try:
        if action == 'encrypt':
            # Convert binary data to base64 string for processing
            if isinstance(data, bytes):
                data_str = base64.b64encode(data).decode('utf-8')
            else:
                data_str = str(data)
            
            # Encrypt the base64 string
            encrypted = getattr(cipher_module, 'encrypt')(data_str, key)
            
            # Return as bytes
            if isinstance(encrypted, str):
                return encrypted.encode('utf-8')
            return encrypted
            
        elif action == 'decrypt':
            # Convert bytes to string for decryption
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='ignore')
            else:
                data_str = str(data)
                
            # Decrypt
            decrypted = getattr(cipher_module, 'decrypt')(data_str, key)
            
            try:
                # Try to decode from base64 (original binary data)
                return base64.b64decode(decrypted)
            except Exception:
                # If not base64, return as text
                if isinstance(decrypted, str):
                    return decrypted.encode('utf-8')
                return decrypted
                
    except Exception as e:
        raise Exception(f"Error dalam pemrosesan file: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Simpan state form
        form_state = {
            'text_input': request.form.get('text_input', ''),
            'key_input': request.form.get('key', ''),
            'cipher_choice': request.form.get('cipher', 'shift'),
            'input_type': request.form.get('input_type', 'text')
        }
       
        try:
            action = request.form.get('action')
            cipher_choice = request.form.get('cipher')
            key = request.form.get('key', '').strip()
            input_type = request.form.get('input_type')
            
            # Validasi input dasar
            if not all([action, cipher_choice, key]):
                flash("Semua field harus diisi!", "danger")
                return render_template('index.html', **form_state)
            
            cipher_module = CIPHER_MAP.get(cipher_choice)
            if not cipher_module:
                flash("Cipher tidak valid!", "danger")
                return render_template('index.html', **form_state)
            
            # Validasi khusus untuk permutation cipher
            if cipher_choice == 'permutation':
                try:
                    # Cek apakah key adalah angka yang dipisah spasi
                    key_numbers = [int(x) for x in key.split()]
                    # Validasi bahwa angka-angka adalah permutasi valid
                    if not key_numbers or len(set(key_numbers)) != len(key_numbers):
                        flash("Key permutation harus berupa angka unik dipisah spasi (contoh: 3 1 4 2)", "danger")
                        return render_template('index.html', **form_state)
                except ValueError:
                    flash("Key permutation tidak valid! Gunakan format: 3 1 4 2", "danger")
                    return render_template('index.html', **form_state)
            
            # Process text input
            if input_type == 'text':
                data = request.form.get('text_input', '').strip()
                if not data:
                    flash("Input teks tidak boleh kosong!", "danger")
                    return render_template('index.html', **form_state)
               
                try:
                    process_function = getattr(cipher_module, action)
                    processed_data = process_function(data, key)
                   
                    # Format output untuk readability
                    if action == 'encrypt' and isinstance(processed_data, str):
                        processed_data = ' '.join(processed_data[i:i+5] for i in range(0, len(processed_data), 5))
                   
                    form_state['result'] = processed_data
                    return render_template('index.html', **form_state)
                    
                except Exception as e:
                    flash(f"Error pemrosesan teks: {str(e)}", "danger")
                    return render_template('index.html', **form_state)
           
            # Process file input
            else:
                if 'file_input' not in request.files:
                    flash("File input tidak ditemukan!", "danger")
                    return render_template('index.html', **form_state)
                    
                file = request.files['file_input']
                
                if not file or file.filename == '':
                    flash("File belum dipilih!", "danger")
                    return render_template('index.html', **form_state)
               
                original_filename = secure_filename(file.filename)
                if not original_filename:
                    original_filename = "unknown_file"
                
                # Baca file data
                try:
                    file_data = file.read()
                    if not file_data:
                        flash("File kosong!", "danger")
                        return render_template('index.html', **form_state)
                        
                except Exception as e:
                    flash(f"Error membaca file: {str(e)}", "danger")
                    return render_template('index.html', **form_state)
                
                # Process berdasarkan action
                if action == 'encrypt':
                    try:
                        # Process file content
                        encrypted_content = process_file_content(file_data, cipher_module, 'encrypt', key)
                        
                        # Siapkan output dengan filename
                        filename_bytes = original_filename.encode('utf-8')
                        filename_length = len(filename_bytes)
                        
                        # Batasi panjang filename untuk keamanan
                        if filename_length > 255:
                            filename_bytes = filename_bytes[:255]
                            filename_length = 255
                        
                        # Format: [filename_length][filename][encrypted_content]
                        output_data = bytes([filename_length]) + filename_bytes + encrypted_content
                        output_filename = original_filename + '.enc'
                        
                        return send_file(
                            io.BytesIO(output_data), 
                            as_attachment=True, 
                            download_name=output_filename,
                            mimetype='application/octet-stream'
                        )
                        
                    except Exception as e:
                        flash(f"Error enkripsi file: {str(e)}", "danger")
                        return render_template('index.html', **form_state)
                
                elif action == 'decrypt':
                    try:
                        # Validasi ukuran file minimum
                        if len(file_data) < 2:
                            flash("File terenkripsi tidak valid!", "danger")
                            return render_template('index.html', **form_state)
                        
                        # Parse format file terenkripsi
                        filename_length = file_data[0]
                        
                        if len(file_data) < 1 + filename_length:
                            flash("Format file terenkripsi salah!", "danger")
                            return render_template('index.html', **form_state)
                        
                        # Extract filename dan encrypted content
                        filename_bytes = file_data[1:1+filename_length]
                        encrypted_content = file_data[1+filename_length:]
                        
                        try:
                            output_filename = filename_bytes.decode('utf-8')
                        except UnicodeDecodeError:
                            output_filename = "decrypted_file"
                        
                        # Decrypt content
                        decrypted_data = process_file_content(encrypted_content, cipher_module, 'decrypt', key)
                        
                        return send_file(
                            io.BytesIO(decrypted_data), 
                            as_attachment=True, 
                            download_name=output_filename,
                            mimetype='application/octet-stream'
                        )
                        
                    except Exception as e:
                        flash(f"Error dekripsi file: {str(e)}", "danger")
                        return render_template('index.html', **form_state)
       
        except Exception as e:
            flash(f"Terjadi error: {str(e)}", "danger")
            return render_template('index.html', **form_state)
           
    return render_template('index.html')

@app.errorhandler(413)
def too_large(e):
    flash(f"File terlalu besar! Maksimal {MAX_FILE_SIZE // 1024 // 1024}MB", "danger")
    return render_template('index.html'), 413

@app.errorhandler(500)
def internal_error(e):
    flash("Terjadi kesalahan internal server", "danger")
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(debug=True)