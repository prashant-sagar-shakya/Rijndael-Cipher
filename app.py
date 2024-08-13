from flask import Flask, render_template, request, redirect, url_for, flash
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Rijndael cipher configuration
BLOCK_SIZE = 16  # AES block size is fixed at 16 bytes


def encrypt(plain_text, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), BLOCK_SIZE))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ct


def decrypt(cipher_text, key):
    try:
        iv = base64.b64decode(cipher_text[:24])
        ct = base64.b64decode(cipher_text[24:])
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), BLOCK_SIZE)
        return pt.decode('utf-8')
    except (ValueError, KeyError):
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        text = request.form.get('text')
        key = request.form.get('key')

        if len(key) not in [16, 24, 32]:
            flash('Key must be 16, 24, or 32 bytes long.')
            return redirect(url_for('index'))

        if action == 'encrypt':
            result = encrypt(text, key)
            flash(f'Encrypted: {result}')
        elif action == 'decrypt':
            result = decrypt(text, key)
            if result is None:
                flash('Decryption failed. Invalid ciphertext or key.')
            else:
                flash(f'Decrypted: {result}')
        return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
