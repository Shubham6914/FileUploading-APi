# your_app/utils.py

import hashlib
import time
from django.conf import settings
from django.urls import reverse

# def generate_encrypted_url(download_link):
#    file_id = download_link.file.id
#    client_user_id = download_link.client_user.id
#    timestamp = int(time.time())
#    raw_string = f"{file_id}-{client_user_id}-{timestamp}-{settings.SECRET_KEY}"
#    encrypted_string = hashlib.sha256(raw_string.encode()).hexdigest()
#    encrypted_url = reverse('download_file', kwargs={'encrypted_string': encrypted_string})
#    return encrypted_url

import hashlib
import base64

def generate_encrypted_url(download_link):
    # Example encryption logic
    base_string = f"{download_link.file.id}-{download_link.client_user.id}-{download_link.expires_at}"
    encrypted_bytes = hashlib.sha256(base_string.encode('utf-8')).digest()
    encrypted_url = base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8').rstrip('=')
    return encrypted_url


from cryptography.fernet import Fernet

def decrypt_url(encrypted_string):
    key = b'your-secret-key'  # Replace with your actual key
    cipher_suite = Fernet(key)
    decrypted_bytes = cipher_suite.decrypt(encrypted_string.encode())
    decrypted_string = decrypted_bytes.decode()
    return decrypted_string
