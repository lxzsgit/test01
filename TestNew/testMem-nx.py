import os
import re
import xlwt
import time
import datetime

workbook = xlwt.Workbook()
style = xlwt.XFStyle()
style.num_format_str = 'h:mm:ss'
pck = "com.nx2x.diq"
file = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

def get_mem():
    '''定义变量，进程总数，进程数组'''
    j = 1
    i = 1
    processSum=0
    processList=[]
    worksheet = workbook.add_sheet('MySheet2')
    worksheet.write(0, 0, '时间')
    contents = os.popen("adb shell ps| findstr " + pck).readlines()

    while i < runtime*20:
        '''每三秒获取一次内存值'''
        worksheet.write(i, 0, datetime.datetime.now(),style)
        # print(contents)
        j = 0
        while j < len(contents):
            if contents[j] == '\n':
                j = j + 1
            else:
                ''''遍历应用所有进程的pid'''

                pid = contents[j].split()[1]
                try:
                    proc = re.search('(com.+)\n', contents[j]).group(1)
                except AttributeError:
                    break
                # proc = contents[j].split()[8]
                '''遍历所有进程的内存值'''
                b = os.popen('adb shell dumpsys meminfo ' + pid)
                c = b.read()
                d = re.search(r'(TOTAL)\s*(\d{0,8})', c)
                try:
                    mem = round(int(d.group(2)) / 1024, 2)
                except AttributeError:
                    mem = 0
                    pass
                print(proc + '内存值：' + str(mem))
                j = j+1
                name=str(pid)+proc
                if name not in processList:
                    processSum=processSum+1
                    worksheet.write(0, processSum, name)
                    processList.append(name)
                processIndex=processList.index(name)
                if processIndex != -1:
                   worksheet.write(i, processIndex+1, mem)
                workbook.save('d:/' + file + '.xlsx')
        i = i + 1
        time.sleep(3)
    print('测试完毕。')

if __name__ == "__main__":
    runtime = float(input("请输入测试时间："))
    get_mem()



