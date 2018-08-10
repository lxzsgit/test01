#安装双开助手，调出所有的广告，back出去等待五分钟，查询一次内存数据，然后back再进100次，等待五分钟，再查询一次内存数据
import time
import re
import sys
from termcolor import *
import startn

os.popen('adb shell am start -W com.excelliance.dualaid/com.excelliance.kxqp.ui.HelloActivity')
time.sleep(2)
os.popen('adb shell input keyevent 4')
path = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
try:
    os.mkdir('d:/testMem')
except FileExistsError:
    pass
#
# def get_pid():
#     s = os.popen('adb shell ps | findstr ' + 'com.excelliance').readlines()
#     print(s)


def WaitMin():
    h = 0
    while h < 300:
        sys.stdout.write(str(300 - h) + " → ")
        sys.stdout.flush()
        time.sleep(10)
        h = h + 10
    else:
        print("0")
    print('\n')
    b = os.popen('adb shell dumpsys meminfo com.excelliance.dualaid')
    c = b.read()
    print(c)
    d = re.search(r'(TOTAL)\s*(\d{0,8})\s*\d*\s*\d*\s*\d*\s*(\d{0,8})', c)
    pssresu = round(int(d.group(2))/1024, 2)
    heapresu = round(int(d.group(3))/1024, 2)
    p = str(pssresu)
    h = str(heapresu)
    print("——"*29)
    print("PSS TOTAL值为：", colored(p, "red") + "MB" + '\n' + "Heap Size值为：", colored(h, "red") + "MB")
    with open('d:/testMem/' + path + '.txt', 'a') as f:
        f.write("Pss Total值：" + p + "MB" + '\n')
        f.write("Heap Size值：" + h + "MB" + '\n')
    print("——"*29)

def BackHundred():
    startn.back_test(100)
    print("100次执行完毕。")

if __name__ == "__main__":
    WaitMin()
    BackHundred()
    WaitMin()
