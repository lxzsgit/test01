import os
import re
import time

from termcolor import colored


def test_device():
    t = os.popen('adb devices').read()
    try:
        t_device = re.search(r'^([a-zA-Z0-9]+)\s+device', t, re.M).group(1)
    except AttributeError:
        t_device = None
        print(colored("设备未连接，请检查……", "red"))
        time.sleep(3)
        test_device()


def get_pckname():
    '''获取当前应用包名'''
    test_device()
    pattern = re.compile(r"[a-zA-Z0-9.]+/.[a-zA-Z0-9.]+")
    os.popen("adb wait-for-device")
    out = os.popen("adb shell dumpsys input | findstr FocusedApplication").read()
    pckname= pattern.findall(out)[0].split("/")[0]
    return pckname


def get_activity():
    '''获取应用类名'''
    pattern = re.compile(r"[a-zA-Z0-9.]+/.[a-zA-Z0-9.]+")
    os.popen("adb wait-for-device")
    out = os.popen("adb shell dumpsys input | findstr FocusedApplication").read()
    activity = pattern.findall(out)[0].split("/")[1]
    return activity

# def get_pid():
#     '''获取应用pid'''
#     content = os.popen("adb shell ps| findstr -e " + pck).read()
#     pid = content.split()[1]
#     return pid


def import_apk(name):
    package = os.popen("adb shell pm list packages -f " + name).read()
    Gpath = re.search(r'(/\S+\.apk)', package)
    path = Gpath.group(1)
    b = os.popen("adb pull " + path + " d:/apk/" + get_pckname() + '.apk').read()
    try:
        ss = re.search('pulled', b)
        print('done!')
    except AttributeError:
        print('导入包未完成！')
        pass

    # print('done!')


if __name__ == "__main__":
    print(get_pckname())
    print(get_activity())
    ch = input('是否需要导出包？y/n')
    if ch == 'Y' or ch == 'y':
        import_apk(get_pckname())
    else:
        pass
