# coding:utf-8
import os
import json
import markdown


with open("../test_md.md", "w", encoding="utf-8") as cf:
    for root, dirs, files, in os.walk("../../json_files", topdown=False):
        for f_name in files:
            file = root + "/" + f_name
            with open(file, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
                abi = data.get("abi", None)
                contract_address = data.get("contract_address", None)
            # f_name = f_name.split(".")[0].split("_")[1]
            show_f_name = f_name.split(".")[0]
            cf.write("# 合约名: " + show_f_name + "\n")
            cf.write("\n")
            cf.write("# 合约地址: " + contract_address + "\n")
            cf.write("\n")
            cf.write("函数名|参数名|参数类型|返回|返回类型|说明")
            cf.write("\n")
            cf.write(":--:|:--:|:--:|:--:|:--:|:--")
            for t in abi:
                cf.write("\n")
                if t["type"] == "function":
                    s_func = t["name"]
                    s_input = [it for it in t["inputs"]]
                    s_input1 = [it['name'] for it in t["inputs"]]
                    s_func = s_func + "(" + ','.join(s_input1) + ")"
                    s_return = t["outputs"]
                    cf.write(s_func + "|")
                    if s_input:
                        name_l = []
                        type_l = []
                        for i in s_input:
                            name_l.append(i["name"])
                            type_l.append(i["type"])
                        cf.write(",".join(name_l) + "|")
                        cf.write(",".join(type_l) + "|")
                    else:
                        cf.write("无" + "|")
                        cf.write("无" + "|")
                    if s_return:
                        name_l = []
                        type_l = []
                        for i in s_return:
                            name_l.append(i["name"])
                            type_l.append(i["type"])
                        cf.write(",".join(name_l) + "|")
                        cf.write(",".join(type_l) + "|")

                    else:
                        cf.write("无" + "|")
                        cf.write("无" + "|")
                    
                    

