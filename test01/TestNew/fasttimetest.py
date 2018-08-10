import os
import re
from termcolor import colored
import time

pkgName = "com.excelliance.dualaid"
pkgActName = "com.excelliance.kxqp.ui.HelloActivity"
while 1:
    while 1:
        try:
            ver1, ti = map(str, input('请输入版本号和执行次数，空格隔开：').split())
            break
        except ValueError:
            print(colored('请检查输入内容是否完整或版本号与执行次数间是否加了空格！', 'red'))
    if int(ti) >= 3:
        break
    else:
        print(colored('执行次数不能小于3！', 'red'))
times = int(ti) + 1

path = time.strftime('%Y%m%d%H%M%S-', time.localtime(time.time()))

class testTime(object):
    def testforce(self):
        fpath = 'd:/testTime/force/'
        p = os.popen('adb shell am start -S -R ' + str(times) + ' -W com.excelliance.dualaid/com.excelliance.kxqp.ui.HelloActivity')
        s = p.read()
        b = re.findall(r'TotalTime:\s(\d+)', s)
        print(b)
        c = []
        for x in b:
            c.append(int(x))
        print('启动时间结果：' + str(c))
        sum = 0
        for i in c:
            sum = sum + i
        print("总和：" + str(sum))

        avg = round((sum - max(c) - min(c))/(int(ti)-2), 3)
        print("最大值为：" + str(max(c)))
        print('平均值为：' + colored(str(avg), 'red'))

        with open(fpath + path + ver1 + '.txt', 'a') as f:
            f.write('启动时间：' + str(c))
            f.write('\n' + "平均值：" + str(avg))


testTime().testforce()