# coding:utf-8
from my_dispatcher import api_add
from util.dbmanager import db_manager
from util.mysql_db import Apps
from cert.eth_certs import EthCert


@api_add
def add_app(*args, **kwargs):
    ec = EthCert("hyf_app")
    ec.generate(4096)
    cli_pbk = ec.public_key_str
    cli_prk = ec.private_key_str
    ec.save_file()
    
    ec1 = EthCert("hyf_srv")
    ec1.generate(4096)
    srv_pbk = ec1.public_key_str
    srv_prk = ec1.private_key_str
    ec1.save_file()
    
    session = db_manager.master()
    new_app = Apps(appid="hyf_app", ip=["localhost"], ns=["127.0.0.1"],
                   cli_publickey=cli_pbk, cli_privatekey=cli_prk, status=1,
                   srv_publickey=srv_pbk, srv_privatekey=srv_prk, desc="xxxx", srv="xxx")
    session.add(new_app)
    session.commit()
    session.close()
    return "add app ok"


def leslie():
    ec = EthCert()
    cli_privatekey = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
"""
    srv_publickey = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAzEJHrDDV8vlpnn8Bu1R1
m1yIGmkObIgJ9A4ukNXBGaMUh6cxTowSsoM6klbWiXr14a8pdBzbSqdQ17KEc4F2
Y3zZriQwI+dmPEIENwyhrhZaOGh8AnatuxOKolIkD/ovYSNdVDsRkEJq5WHjqmSk
PPrR5ViIYMjpB2LpXMlEzTMc+i9qa/8mXEBwwuNKqOaFN6InfGwuLvkx6VFqzbdy
TfpQ9ZLEO6DI3RvlGW+yMz5OMRUBou3eAVOI9VFsxzk1SunPwtu64vtNg6wJPui5
hRya+WAAvWkvyuMkFPSQcyPI4E71h5PJvgn++U6u8ghY4wRFXuwXuzV6aj+5Qa84
IgBUPZr4y3dkl8FIC4G9WTth6JfsmM+8KvYwnGiqI9EYXf7xJvUOCTQrOus8uRAK
evuB4LwOLI1MlRH+vigkShVLxBMcz2Kzs0Punspu1cc5gkeO0IpjFofpDY5M+Kul
zGixZfZ6dQs3nJIJsgzOLqNayD16N2iLYjM3j8/Xjl3BihWMwhMjCzxjXhBv/iRC
GLkcp/u+YFW4Ivw+MwqhKrMRLNY/JnYXYP4RUpT0f3Oc3/r/UeKIG/hejTi15xJ2
ckOaNhUHHq75+H1JQBaExFu4C3pZVfFeALiNGQq5LuJzGTRbeiIohwIEF7Q8MJgw
gBBbdiFfwsLJLqlHzEIR0u8CAwEAAQ==
-----END PUBLIC KEY-----
"""
    ec.init_key(public_key_str=srv_publickey, private_key_str=cli_privatekey)
    data = {
        "params": {
            "appid": "Canigreen",
         }
    }
    ec.serialization()
    sign = ec.sign(data)
    print(sign)
    encrypt = ec.encrypt(data)
    print(encrypt)


if __name__ == "__main__":
    leslie()










