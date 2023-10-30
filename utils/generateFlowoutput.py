from promptflow import tool

@tool
def Flow4output1(output1:str = "",output2:str ="",output3:str="",output4:str=""):
    result = ""
    for content in [output1,output2,output3,output4]:
        result += content
    return result