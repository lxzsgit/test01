import os
import re
import xlwt
import time
import datetime

workbook = xlwt.Workbook()
style = xlwt.XFStyle()
style.num_format_str = 'h:mm:ss'

content = os.popen("adb shell ps| findstr -E " + "com.excelliance.dualaid.vend").read()
pid = content.split()[1]

def runtime():
    i = 0
    worksheet = workbook.add_sheet('MySheet2')
    worksheet.write(0, 0, '时间')
    worksheet.write(0, 1, '内存值')
    while i < 720:
        i = i + 1
        b = os.popen('adb shell dumpsys cpuinfo |findstr ' + pid)
        c = b.read()
        print(c)
        d = re.search(r'([0-9]{0,1}[0-9]{0,1}[.][1-9]{0,1}\%|[0-9]{0,1}[0-9]{0,1}\%)\s\d{0,5}.', c)
        try:
            r = d.group(1)
        except AttributeError:
            r = None
            pass
        print("第", i, "次的值：", r)
        worksheet.write(i, 0, datetime.datetime.now(), style)
        worksheet.write(i, 1, r)
        time.sleep(5)
        workbook.save('d:/cpuresult1.xlsx')
    print('运行时测试完毕。')

if __name__ == "__main__":
    # wechat()
    runtime()

