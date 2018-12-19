# coding:utf-8
import os
import json
import markdown


with open("../contracts_func.md", "w", encoding="utf-8") as cf:
    for root, dirs, files, in os.walk("../../json_files", topdown=False):
        for f_name in files:
            file = root + "/" + f_name
            with open(file, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
                abi = data.get("abi", None)
                contract_address = data.get("contract_address", None)
                function_list = []
            f_name = f_name.split(".")[0].split("_")[1]
            cf.write("# 合约名: " + f_name + "\n")
            cf.write("\n")
            for t in abi:
                md_str = ""
                if t["type"] == "function":
                    s_func = t["name"]
                    s_input = [it for it in t["inputs"]]
                    s_input1 = [it['name'] for it in t["inputs"]]
                    s_func = s_func + "(" + ','.join(s_input1) + ")"
                    s_return = t["outputs"]
                    cf.write("## " + s_func + "\n")
                    if s_input:
                        cf.write("参数类型:" + "\n")
                        cf.write("\n")
                        for i in s_input:
                            cf.write(i['name'] + "--->" + i['type'] + "\n")
                            cf.write("\n")
                            
                    if s_return:
                        cf.write("返回值:" + "\n")
                        cf.write("\n")
                        for i in s_return:
                            cf.write(i['type'] + "\n")
                            
                    else:
                        cf.write("返回值: 无" + "\n")
                    

