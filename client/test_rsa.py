zBytes = "hyf"
#zBytes = "YAY!! We Are Going To Make Ethereum & Python Great! Go Crypto and Blockchain and DAG, etc...!!!"
len1 = len(zBytes)
if len1 > 32:
    print('input string length: '+ str(len1)+ ' is too long')
    zBytes32 = zBytes[:32]
else:
    print('input string length: '+ str(len1)+ ' is too short')
    print('More characters needed: '+ str(32-len1))
    zBytes32 = zBytes.ljust(32, '0')
print('zBytes32 = '+ str(zBytes32)+ ' and its length: '+ str(len(zBytes32)))
xBytes32 = bytes(zBytes32, 'utf-8')
print('xBytes32 = '+ str(xBytes32))
# contractInstance.functions.yourFunctionName(xBytes32).buildTransaction()

print(b'hyf00000000000000000000000000000'.decode("utf-8"))