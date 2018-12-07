# coding:utf-8
import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class EthCert(object):

    def __init__(self, username):
        cert_dir = os.path.dirname(os.path.realpath(__file__))
        self.pems = os.path.join(cert_dir, "pems")
        self.pems_user_dir = os.path.join(self.pems, username)
        if not os.path.isdir(self.pems_user_dir):
            os.mkdir(self.pems_user_dir)
        self.thiscert = {
            "private": os.path.join(self.pems, username, "private_key.pem"),
            "public": os.path.join(self.pems, username, "public_key.pem"),
        }
        self.private_key = None
        self.public_key = None
        self.style = None
        self.error = ""

    def load_private_public_key(self):
        try:
            with open(self.thiscert['private'], 'rb') as kfd:
                self.private_key = serialization.load_pem_private_key(
                    kfd.read(),
                    password=None,
                    backend=default_backend()
                )
            with open(self.thiscert['public'], 'rb') as kfd:
                self.public_key = load_pem_public_key(kfd.read(), default_backend())
        except Exception as e:
            self.error = f"{e}"
            return False
        return True

    def load_private_key(self):
        try:
            with open(self.thiscert['private'], 'rb') as kfd:
                self.private_key = serialization.load_pem_private_key(
                    kfd.read(),
                    password=None,
                    backend=default_backend()
                )
        except Exception as e:
            self.error = f"{e}"
            return False
        return True

    def load_public_key(self):
        try:
            with open(self.thiscert['public'], 'rb') as kfd:
                self.public_key = load_pem_public_key(kfd.read(), default_backend())
        except Exception as e:
            self.error = f"{e}"
            return False
        return True

    def convert(self, origin_str):
        if isinstance(origin_str, bytes):
            return origin_str
        if isinstance(origin_str, str):
            return bytes(origin_str, encoding='utf8')
        else:
            return bytes(str(origin_str), encoding='utf8')

    def generate(self, size=2048):
        # Generate the public/private key pair.
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=size,
            backend=default_backend(),
        )
        self.private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        self.public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return True

    def save(self):
        try:
            # Save the private key to a file.
            with open(self.thiscert['private'], 'wb') as f:
                f.write(self.private_key)
            # Save the public key to a file.
            with open(self.thiscert['public'], 'wb') as f:
                f.write(self.public_key)
        except Exception as e:
            self.error = f"{e}"
            return False
        return True

    def sign(self, origin_data):
        if self.private_key is None:
            self.error = "load private key first"
            return False
        signature = base64.b64encode(
            self.private_key.sign(
                self.convert(origin_data),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        )
        return signature

    def sign2(self, origin_data):
        if self.private_key is None:
            self.error = "load private key first"
            return False
        signature = base64.b64encode(self.private_key.sign(
                self.convert(origin_data),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        )
        return signature

    def verify(self, origin_data, signature):
        if self.public_key is None:
            self.error = "load public key first"
            return False
        signature_decode = base64.b64decode(signature)
        try:
            self.public_key.verify(
                signature_decode,
                self.convert(origin_data),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        except InvalidSignature as e:
            self.error = f'ERROR: signature failed verification! {e}'
            return False
        return True

    def verify2(self, origin_data, signature):
        if self.public_key is None:
            self.error = "load public key first"
            return False
        signature_decode = base64.b64decode(signature)
        try:
            self.public_key.verify(
                signature_decode,
                self.convert(origin_data),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        except InvalidSignature:
            self.error = "ERROR: signature failed verification!"
            return False
        return True

    def encrypt(self, origin_data):
        encrypt_data_encode = base64.b64encode(self.public_key.encrypt(
                self.convert(origin_data),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                )
            )
        )
        return encrypt_data_encode

    def decrypt(self, encrypt_data):
        try:
            encrypt_data_decode = base64.b64decode(encrypt_data)
            decrypt_data = self.private_key.decrypt(
                self.convert(encrypt_data_decode),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                )
            )
        except Exception as e:
            self.error = f"ERROR: Decryption failed! {e}"
            return False
        return decrypt_data


if __name__ == "__main__":
    ec = EthCert("zzy")
    # 生成私钥与公钥, 长度默认为2048
    ec.generate(4096)
    if not ec.save():
        print(ec.error)
    # 加载private/public
    # ec.load_private_key()
    # ec.load_public_key()
    if ec.load_private_public_key():
        origin = "XiaMen City"
        # 数据签名与验证方式一
        sign = ec.sign(origin)
        print(ec.verify(origin, sign))
        # 数据签名与验证方式二
        sign = ec.sign2(origin)
        print(ec.verify2(origin, sign))
        # 加密数据
        edata = ec.encrypt(origin)
        # 解密数据
        ddata = ec.decrypt(edata)
        print(ddata)
    else:
        print(ec.error)





