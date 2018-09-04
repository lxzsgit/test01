import os
import time
import urllib

from FunctionTest.func_script.func_lib import AppiumInit
from FunctionTest.func_script.func_lib import AppOperation


class AppiumServerCheck(object):
    appium = AppiumInit()
    ap_opr = AppOperation()

    def check_appium_server(self):
        # 检测appium服务是否已开启，如未开启则自动开启服务进行初始化
        # 如已开启直接进行初始化
        if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
            while True:
                try:
                    self.appium.appium_init()
                    break
                except ConnectionRefusedError:
                    time.sleep(3)
                except urllib.error.URLError:
                    time.sleep(3)
            self.ap_opr.force_stop('com.excelliance.dualaid')
            print('测试环境OK，开始执行测试\n')
        else:
            os.popen("start appium")
            print("正在启动appium服务程序，请稍后...\n")
            while True:
                if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
                    while True:
                        try:
                            self.appium.appium_init()
                            break
                        except ConnectionRefusedError:
                            time.sleep(3)
                        except urllib.error.URLError:
                            time.sleep(3)
                    self.ap_opr.force_stop('com.excelliance.dualaid')
                    print('测试环境OK，开始执行测试\n')
                    break
                else:
                    time.sleep(3)

    def stop_appium_server(self):
        # 结束appium进程（Windows适用）
        pid_node = os.popen('tasklist | findstr "node.exe"').readlines()
        for i in pid_node:
            os.popen('taskkill /f /pid ' + i.split()[1])
        pid_cmd = os.popen('tasklist | findstr "cmd.exe"').readlines()
        for i in pid_cmd:
            os.popen('taskkill /f /pid ' + i.split()[1])


if __name__ == '__main__':
    ap_ser_che = AppiumServerCheck()
    ap_ser_che.check_appium_server()
    ap_ser_che.stop_appium_server()
