"""
编写一个文件拷贝程序,将一个文件拷贝一份,重新取另外一个名字(自定).
      文件可能是文本,也可能是二进制
"""

filename = input("文件:")

fr = open(filename,'rb')
fw = open("备份-"+filename,'wb')

while True:
    # 循环读取
    data = fr.read(1024)
    if not data:  # 文件结束
        break
    fw.write(data)

fr.close()
fw.close()
