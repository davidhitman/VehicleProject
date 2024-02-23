import random

class helper:
    @staticmethod
    def encrypt_password(user_password):
        random_string = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=len(user_password) * 2))
        encrypted_password = ""

        for i in range(len(user_password)):
            encrypted_password += random_string[2 * i:2 * i + 2] + user_password[i]

        return "^^" + encrypted_password + "$$"

    @staticmethod
    def decrypt_password(password):
        encrypted_password = password[2:-2] 
        user_password = ''
        for i in range(0, len(encrypted_password), 3):
            user_password += encrypted_password[i+2]
        return user_password

# hlp = helper()
# decrypted_password = hlp.dec("^^6wD9shl8a7UnZo00E5IP0QH8$$")
# print(decrypted_password)
