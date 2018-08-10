import os
import time
import re
from termcolor import colored

try:
    os.makedirs(r'd:/fpstest')
    print('测试文件夹已创建')
except FileExistsError:
    pass

i = 0
path = time.strftime('%Y%m%d%H%M%S-', time.localtime(time.time()))
bpath = 'd:/fpstest/'

os.popen('adb shell am force-stop com.excelliance.dualaid')
print('请操作要测应用！')
time.sleep(3)


def testDevice():
    t = os.popen('adb devices').read()
    try:
        tdevice = re.search(r'^([a-zA-Z0-9]+)\s+device', t, re.M).group(1)
    except AttributeError:
        tdevice = None
        print(colored("设备未连接，请检查……", "red"))
        time.sleep(3)
        testDevice()
    return tdevice

# def get_topActivity():
#     s = os.popen('adb shell dumpsys SurfaceFlinger | findstr "|....|"').read()
#     ta = re.findall('com.*', s, re.M)
#     return ta[0]
#
# def get_something():
#     a = get_topActivity()
#     os.popen('adb shell dumpsys SurfaceFlinger --latency-clear SurfaceView')
#     b = os.popen('adb shell dumpsys SurfaceFlinger --latency ' + a).read()
#     print(b)
# get_something()
while i <= 30:
    testDevice()
    f = os.popen('adb shell dumpsys gfxinfo com.excelliance.dualaid').read()
    # print(f)
    s = re.search(r'Profile data in ms:\n([\s\S]+)View hierarchy', f)
    try:
        p = s.group(1)
    except AttributeError:
        print('None')
    fps = s.group(1)
    # print(s.group(1))
    with open(bpath + path + '.txt', 'a') as y:
        y.write('第' + str(i) + '次：' + '\n' + fps)
    i = i + 1
    time.sleep(2)
