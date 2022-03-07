# import binascii
import hashlib
from Crypto.Cipher import AES


class EncryptedWxApkg:
    magic_number = "V1MMWX"
    hash_name = "sha1"
    salt = "saltiest"
    iv = "the iv: 16 bytes"
    xor_key = b"\x66"
    aes_key = ""
    miniprogram_id = ""
    iterations = 1000
    dklen = 32
    full_encrypted_wxapkg_file_path = ""

    def __init__(self, full_encrypted_wxapkg_file_path, miniprogram_id):
        # miniprogram_id should be string like "wx0bad87c71b11ea8c".
        self.miniprogram_id = miniprogram_id
        if len(miniprogram_id) >= 2:
            self.xor_key = miniprogram_id[-2]
        self.aes_key = hashlib.pbkdf2_hmac(self.hash_name, self.miniprogram_id.encode(), self.salt.encode(), self.iterations, self.dklen)
        # self.aes_key = binascii.hexlify(self.aes_key)
        # pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None) -> key
        with open(full_encrypted_wxapkg_file_path, 'rb') as wxapkg_file:
            if not wxapkg_file.read(6).decode() == self.magic_number:
                print("Magic number is not V1MMWX, exit.")
                exit(0)
        self.full_encrypted_wxapkg_file_path = full_encrypted_wxapkg_file_path
    def decrypt_wxapkg(self):
        aes_cipher = AES.new(self.aes_key, AES.MODE_CBC, self.iv.encode())  # use CBC mode
        with open(self.full_encrypted_wxapkg_file_path, 'rb') as wxapkg_file:
            wxapkg_file.seek(6, 1)  # Offset 6 bytes from the start of the file to the end of the file.
            encrypted_data_aes = wxapkg_file.read(1024)
            decrypted_data_aes = aes_cipher.decrypt(encrypted_data_aes)
            with open(self.miniprogram_id, 'wb') as unpack_result:
                unpack_result.write(decrypted_data_aes[0:len(decrypted_data_aes)-1])
                temp = wxapkg_file.read(1)
                while temp:
                    unpack_result.write(bytes(a ^ b for (a, b) in zip(temp, self.xor_key.encode())))
                    temp = wxapkg_file.read(1)


full_encrypted_wxapkg_file_path = "__APP__.wxapkg"
miniprogram_id = "wx0bad87c71b11ea8c"
encrypted_wxapkg_sample = EncryptedWxApkg(full_encrypted_wxapkg_file_path, miniprogram_id)
encrypted_wxapkg_sample.decrypt_wxapkg()

