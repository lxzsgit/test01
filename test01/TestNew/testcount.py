import os
import time

pkgName = "com.excelliance.dualaid"
pkgActName = "com.excelliance.kxqp.ui.HelloActivity"

class testCount(object):
    def test_back11(self):
        a = 1
        while a < 12:
            print("第" + a + "次")
            os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
            time.sleep(2)
            os.popen('adb shell input keyevent 4')
            time.sleep(2)
            a = a + 1
    def test_home1(self):
        a = 1