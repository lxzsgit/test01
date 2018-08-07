import os
import time
import sys
# times = input('请输入执行次数：')
# i = 1
st = 'adb shell am start -W com.excelliance.dualaid/com.excelliance.kxqp.ui.HelloActivity'

def back_test(t):
    os.popen(st)
    time.sleep(2)
    os.popen('adb shell input keyevent 4')
    time.sleep(2)
    i = 1
    while i <= int(t):
        sys.stdout.write("第" + str(i) + "次 ")
        sys.stdout.flush()
        os.popen(st)
        time.sleep(2)
        os.popen('adb shell input keyevent 4')
        time.sleep(2)
        i = i+1
    print('\n')

def home_test(t):
    os.popen(st)
    time.sleep(2)
    os.popen('adb shell input keyevent 3')
    time.sleep(2)
    i = 1
    while i <= int(t):
        sys.stdout.write("第" + str(i) + "次 ")
        sys.stdout.flush()
        os.popen(st)
        time.sleep(2)
        os.popen('adb shell input keyevent 3')
        time.sleep(2)
        i = i + 1
    print('\n')

def force_test(t):
    os.popen(st)
    time.sleep(2)
    os.popen('adb shell am force-stop com.excelliance.dualaid')
    time.sleep(2)
    i = 1
    while i <= int(t):

        sys.stdout.write("第" + str(i) + "次 ")
        sys.stdout.flush()
        os.popen(st)
        time.sleep(2)
        os.popen('adb shell am force-stop com.excelliance.dualaid')
        time.sleep(2)
        i = i + 1
    print('\n')


if __name__ == '__main__':
    times = input('请输入执行次数：')
    back_test(times)

