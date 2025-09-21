import os
import io
from flask import Flask, render_template, request, send_file, flash
from werkzeug.utils import secure_filename

# Impor semua modul cipher
from ciphers import shift_cipher, substitution_cipher, affine_cipher, vigenere_cipher, hill_cipher, permutation_cipher

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

CIPHER_MAP = {
    'shift': shift_cipher,
    'substitution': substitution_cipher,
    'affine': affine_cipher,
    'vigenere': vigenere_cipher,
    'hill': hill_cipher,
    'permutation': permutation_cipher,
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            action = request.form['action']
            cipher_choice = request.form['cipher']
            key = request.form['key']
            input_type = request.form['input_type']

            if not key:
                flash("Kunci tidak boleh kosong!", "perhatian")
                return render_template('index.html')

            data = None
            original_filename = None

            if input_type == 'text':
                data = request.form.get('text_input', '')
                if not data:
                    flash("Input teks tidak boleh kosong!", "perhatian")
                    return render_template('index.html', key_input=key)
            else:
                if 'file_input' not in request.files or request.files['file_input'].filename == '':
                    flash("File belum dipilih!", "perhatian")
                    return render_template('index.html', key_input=key)
                
                file = request.files['file_input']
                original_filename = secure_filename(file.filename)
                data = file.read()

            cipher_module = CIPHER_MAP.get(cipher_choice)
            process_function = getattr(cipher_module, action)
            processed_data = process_function(data, key)

            if input_type == 'text':
                if action == 'encrypt':
                    processed_data = ' '.join(processed_data[i:i+5] for i in range(0, len(processed_data), 5))
                return render_template('index.html', result=processed_data, text_input=data, key_input=key)
            else:
                output_filename = f"{action}ed_{original_filename}"
                if action == 'encrypt':
                    fn_bytes = original_filename.encode('utf-8')
                    output_data = bytes([len(fn_bytes)]) + fn_bytes + processed_data
                    output_filename += '.enc'
                else:
                    fn_len = processed_data[0]
                    output_filename = processed_data[1:1+fn_len].decode('utf-8')
                    output_data = processed_data[1+fn_len:]
                
                return send_file(io.BytesIO(output_data), as_attachment=True, download_name=output_filename)

        except Exception as e:
            flash(f"Terjadi error: {e}", "perhatian")
            return render_template('index.html', text_input=request.form.get('text_input'), key_input=request.form.get('key'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)