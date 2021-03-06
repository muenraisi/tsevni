from inspect import currentframe, getframeinfo


def get_security_resolution(security_code):
    security_code = str(security_code)
    if len(security_code)!=6 and len(security_code)!=5:
        print("security_code",security_code)
        assert (len(security_code) == 6 or len(security_code)==5)
    if len(security_code)==5:
        return "港股通"
    if security_code[0:3] == "300":
        return "创业板"
    elif security_code[0:3] in ["600", "601", "603", "605"]:
        return "沪A股"
    elif security_code[0:3] == "900":
        return "沪B股"
    elif security_code[0:3] == "688":
        return "科创板"
    elif security_code[0:3] == "000":
        return "深A股"
    elif security_code[0:3] == "002":
        return "中小板"
    elif security_code[0:3] == "200":
        return "深B股"
    elif security_code[0:3] in ["700", "080"]:
        return "配股"
    elif security_code[0:3] in ["580", "031"]:
        return "权证"
    elif security_code in ["131800", "131801", "131802", "131803", "131805", "131806", "138109", "131810",
                           "131811"]:
        return "逆回购"
    elif security_code[0:3] == "019":
        return "沪国债"
    elif security_code[0:2] == "10":
        return "深国债"
    elif security_code[0:2] in ["11", "12"]:
        return "可转债"
    elif security_code[0:1] =="7" or security_code[0:2]=="07":
        return "新股新债"
    else:
        file_info = getframeinfo(currentframe())
        exit(file_info.filename + " " + str(file_info.lineno) + ": unknown stock code " + security_code)


if __name__ == "__main__":
    #
    assert (get_security_resolution("688688") == "科创板")
