import os
import re

import time

pkgName = 'com.excelliance.dualaid'
pkgActName = 'com.excelliance.kxqp.ui.HelloActivity'


class Batterytest():
    def reset_batterystats(self):
        print('清除电量信息')
        os.popen('adb shell dumpsys batterystats --reset')

    def off_usb(self):
        print('关闭USB充电状态')
        os.popen('adb shell dumpsys battery unplug')
        os.popen('adb shell dumpsys battery set status 1')

    def app_start(self):
        print('启动应用')
        os.popen('adb shell am start ' + pkgName + '/' + pkgActName)

    def get_uid(self):
        a = os.popen('adb shell ps | findstr ' + pkgName).read()
        b = a.split()[0].replace('_', '')
        return b

    def set_batstatus(self):
        os.popen('adb shell dumpsys battery reset')

    def get_batterystats(self):
        print('获取手机电量信息')
        c = os.popen('adb shell dumpsys batterystats | findstr ' + self.get_uid()).read()
        resu = re.search(r'(Uid.+)\(\s(.+)\s\).*', c)
        result = resu.group(2)
        time.sleep(2)
        # os.popen('adb shell am force-stop ' + pkgName)
        return result

    def result_save(self):
        with open('d:/电量测试.txt', 'a') as f:
            f.write(self.get_batterystats() + '\n')


if __name__ == "__main__":
    Batterytest().reset_batterystats()
    time.sleep(1)
    Batterytest().app_start()
    time.sleep(1)
    Batterytest().get_uid()
    time.sleep(1)
    Batterytest().off_usb()
    time.sleep(1)
    print('开始操作你的应用')
    time.sleep(5)
    Batterytest().set_batstatus()
    time.sleep(1)
    Batterytest().get_batterystats()
    time.sleep(1)
    Batterytest().result_save()
