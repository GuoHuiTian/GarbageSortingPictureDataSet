filename = open("./源垃圾名称.txt",encoding = "utf-8")

str_all=filename.readlines()
list_name=[]
for i in str_all:
    c=i.split(r",")
    c.pop(-1)
    for str1 in c:
        for str2 in str1:
            if str2==r"'" or str2==r" ":
                str1=str1.replace(str2,"")
        list1=str1.split(r"_")
        list_name.append(list1[-1])


with open("./refuse_name.txt","w",encoding="utf-8") as file:
    for str3 in list_name:
        file.write(str3+"\n")


print(list_name)
filename.close()