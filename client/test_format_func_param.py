from web3 import Web3, WebsocketProvider
w3 = Web3(Web3.HTTPProvider("http://192.168.1.14:8101"))


def format_func_param(func_param):
    func_param = func_param.split(",")
    print(func_param)
    t = []
    for f in func_param:
        if isinstance(f, str) and "0x" in f:
            f = "'" + w3.toChecksumAddress(f) + "'"
        t.append(f)
    func_param = ",".join(t)
    return func_param

def format_func_param2(func_param):
    pass

func_param = "0x4b75f75398672BD76587c0Bb1f4Ab7dd3673b9D1, '2', '3'"
func_param = format_func_param(func_param)


account = 1
nonce = 1
func_name = "tSaveMoney"
value = 1
ss1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei(0, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""
print(ss1)

# func_param = ""
# func_param = format_func_param(func_param)
# s1 = f"""contract_instance.functions.{func_name}({func_param}).buildTransaction({{'from': '{account}', 'value': w3.toWei({value}, 'ether'), 'chainId': 1500, 'gas': 2000000, 'gasPrice': 30000000000, 'nonce': {nonce}}})"""

# print(s1)



