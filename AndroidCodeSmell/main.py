# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time:  2021/1/7
@Description: 
"""
if __name__ == "__main__":
    # file = open("C:\\Users\\MaoMorn\\Desktop\\com.tencent.tmgp.sgame\\libGameCore.so", "rb")
    # file_crack = open("C:\\Users\\MaoMorn\\Downloads\\libGameCore.so", "rb")
    # data = file.read(4)
    # count = 0
    # start = 0
    # while data:
    #     data_t = file_crack.read(4)
    #     if data == data_t:
    #         pass
    #     else:
    #         print(data)
    #         print(data_t)
    #         print(hex(count))
    #         print()
    #     count += 4
    #     data = file.read(4)
    # file.close()
    # file_crack.close()
    import torch

    print(torch.__version__)
    print(torch.cuda.is_available())
