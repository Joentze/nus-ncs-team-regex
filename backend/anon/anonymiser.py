"""anonymiser for data"""
import os
import base64
from cryptography.fernet import Fernet
from schemas.Prompt import Prompt

ENCRYPTION_KEY = os.environ["ENCRYPTION_KEY"]


def encrypt_data(input_string: str) -> str:
    """encrypts data"""
    cipher_suite = Fernet(ENCRYPTION_KEY)
    cipher_text = cipher_suite.encrypt(input_string.encode())
    return base64.urlsafe_b64encode(cipher_text).decode()

# Decrypt data using the key


def decrypt_data(cipher_text: bytes) -> str:
    """decrypts cypher"""
    byte_cipher = base64.urlsafe_b64decode(cipher_text).decode()
    cipher_suite = Fernet(ENCRYPTION_KEY)
    plaintext = cipher_suite.decrypt(byte_cipher).decode()
    return plaintext


def encrypt_prompt(prompt: Prompt) -> Prompt:
    """encrypts prompt content before storing in db"""
    return {**prompt.dict(), "content": encrypt_data(prompt.content)}


def decrypt_prompt(prompt: dict) -> Prompt:
    """decrypts prompt content before sending to llm"""
    return {**prompt, "content": decrypt_data(prompt["content"])}


# Example usage
if __name__ == "__main__":
    test_prompt = {"role": "user", "content": "hello there my name is joen"}
    print(encrypt_prompt(test_prompt))
