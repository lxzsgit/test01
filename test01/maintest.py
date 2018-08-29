# _*_ coding:utf-8 _*_
import datetime
import hashlib
import poplib
import re
import shutil
import smtplib
import subprocess
import time
import urllib
from email.header import decode_header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from email.utils import parseaddr
import requests
import selenium
from termcolor import *
from appium import webdriver
import compare_img

# import clear_pic

link_files_path = "D:\\TobTest\\linkfiles\\"
apk_dl_Path = "D:\\TobTest\\apk_dl\\"
log_Path = "D:\\TobTest\\logs\\"
err_apk_path = "D:\\TobTest\\err_app\\"


class AppiumInit(object):
    """appium server"""

    def appium_init(self, apkpath):
        """to initialise appium session"""
        global driver
        getinfo = GetInfo()
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = getinfo.get_android_version()
        desired_caps['deviceName'] = getinfo.get_device_name()
        desired_caps['appPackage'] = getinfo.get_apk_name(apkpath)
        desired_caps['appActivity'] = getinfo.get_apk_activity(apkpath)
        desired_caps['noReset'] = 'true'
        # desired_caps['autoLaunch'] = 'false'
        # desired_caps['unicodeKeyboard'] = 'true'
        # desired_caps['resetKeyboard'] = 'true'
        desired_caps['newCommandTimeout'] = '1232000'
        desired_caps['automationName'] = 'uiautomator2'  # define use uiautomator2 to find element,default is appium
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    def quit(self):
        """to quit this session"""
        driver.quit()

    def confirm_click(self):
        try:
            time.sleep(6)
            driver.find_element_by_android_uiautomator(
                'new UiSelector().resourceIdMatches(".*id/lebian_positiveButton$")').click()
            return True
        except BaseException:
            return False

    def overlay(self):
        """判断是否为覆盖安装"""
        try:
            driver.find_element_by_android_uiautomator('new UiSelector().text("下一步")').click()
        except BaseException:
            pass
        try:
            driver.find_element_by_android_uiautomator('new UiSelector().text("安装")').click()
            print("——————覆盖安装——————")
        except BaseException:
            return False
        return True

    def overlay_launch(self):
        try:
            driver.find_element_by_android_uiautomator('new UiSelector().text("打开")').click()
            print("覆盖安装后启动")
        except BaseException:
            return False
        return True

    def check_appium_server(self):
        # 检测appium服务是否已开启
        if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
            print('Appium已启动')
        else:
            os.popen("start appium")
            print("正在启动appium服务程序，请稍后...")
            while True:
                if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
                    print('appium已启动')
                    break
                else:
                    time.sleep(3)


class GetInfo(object):
    """信息获取"""

    def get_device_name(self):
        """获取设备名称（deviceName）"""
        b = os.popen('adb devices')
        device_name = b.readlines()[1].split()[0]
        return device_name

    def get_android_version(self):
        """获取设备Android版本"""
        c = os.popen('adb shell getprop ro.build.version.release')
        return c.readline()

    def run_shell_cmd(self, cmd, cwd='.'):
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                             shell=True)
        output, err = p.communicate()
        return p.wait(), output, err

    def get_apk_name(self, apkpath):
        """传入测试包所在路径，获取测试包的包名"""
        try:
            status, output, errmsg = self.run_shell_cmd("aapt dump badging \"%s\"" % apkpath)
            ii = str(output)
            a = re.search(r".*package: name='(\S+)' versionCode", ii)
            return a.group(1)
        except AttributeError:
            print("无法获取应用包名！")

    def get_apk_activity(self, apkpath):
        """传入测试包所在路径，获取测试包的启动Activity"""
        try:
            status, output, errmsg = self.run_shell_cmd("aapt dump badging \"%s\"" % apkpath)
            ii = str(output)
            a = re.findall(r"launchable-activity: name='(\S+)'", ii)
            print("应用启动进程为：" + a[0])
            return a[0]
        except IndexError:
            print("无法获取应用启动activity！")

    def get_pid(self, apkname):
        """获取传入的包名的PID"""
        # print(apkname)
        p = os.popen("adb shell ps | findstr \"" + apkname + "\"")
        info = p.readlines()  # 读取命令行的输出到一个list
        for line in info:  # 按行遍历
            lin = line.strip('\n')
            if lin != "":
                s = lin.split(" ")
                while 1:
                    if "" in s:
                        s.remove("")
                    else:
                        break
                if s[-1] == apkname:
                    pid = s[1]
                    return pid


class Emails(object):
    def __init__(self):
        self.username = "zmtest2018@163.com"
        self.password = "zmzmzm123"
        self.receiver = "xuhe@excelliance.cn,wangzhihai@excelliance.cn,wenchunhe@excelliance.cn,guoxueli@excelliance.cn,jingchaojie@excelliance.cn,lixianzhuang@excelliance.cn"
        # self.receiver = "lixianzhuang@excelliance.cn"

    def decode_str(self, ss):
        if not ss:
            return None
        value, charset = decode_header(ss)[0]
        if charset:
            value = value.decode(charset)
        return value

    def del_mail(self):
        host = 'pop.163.com'
        # server = poplib.POP3(host, port=110)
        while 1:
            try:
                server = poplib.POP3_SSL(host)
                break
            except TimeoutError:
                print("连接超时，4分钟后重试")
                time.sleep(240)
        server.user(self.username)
        server.pass_(self.password)
        # 获得邮件
        first = len(server.list()[1])
        server.dele(first)
        server.quit()

    def get_mails(self):
        """邮件获取存有下载链接的txt文件"""
        host = 'pop.163.com'
        # server = poplib.POP3_SSL(host)  # ,port=110,timeout=1000
        while 1:
            try:
                server = poplib.POP3_SSL(host)
                break
            except TimeoutError:
                print("连接超时，5分钟后重试")
                time.sleep(300)

        server.user(self.username)
        server.pass_(self.password)
        # 获得邮件
        first = len(server.list()[1])
        # 获取最新的一封邮件
        message = server.retr(first)
        message = b'\r\n'.join(message[1]).decode()
        message = Parser().parsestr(message)
        date = message.get('Date')
        print("====" * 10)
        subject = message.get('Subject')
        subject = self.decode_str(subject)
        print(subject)
        # 如果标题匹配
        value = message.get('From')
        if value:
            hdr, addr = parseaddr(value)
            name = self.decode_str(hdr)
            value = u'%s <%s>' % (name, addr)
        for part in message.walk():
            # print(part.get_content_type())
            fileName = part.get_filename()
            fileName = self.decode_str(fileName)
            if fileName == "prevercode.txt" or value == "notify@excean.com":
                # 保存附件
                with open(os.path.join(link_files_path, fileName), 'wb') as fEx:
                    data = part.get_payload(decode=True)
                    fEx.write(data)
                    print("日期：%s" % date)
                    print("发件人: %s" % value)
                    print("标题:%s" % subject)
                    print("附件%s已保存" % fileName)
                return True
        server.quit()

    def send_email(self, sub, imgpath, *dl_url):
        """发送带图片的邮件"""
        email_host = 'smtp.163.com'  # 邮箱服务器地址
        # 发送者密码是邮箱的授权码，不是登录的密码
        msg = MIMEMultipart('related')
        msg['Subject'] = sub
        msg['From'] = self.username
        msg['To'] = self.receiver
        att = MIMEApplication(
            open(log_Path + "applog.txt", 'rb').read())
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="appy.log"'
        msg.attach(att)

        with open(imgpath, 'rb') as sendimagefile:
            image = MIMEImage(sendimagefile.read())
        image.add_header('Content-ID', imgpath)
        msg.attach(image)

        ll = str(dl_url[0])[0]
        # print(ll)

        if ll == 'h':
            mail_img = """
                    <p>该包下载链接：<a href=""" + str(dl_url[0]) + """ target="_blank">""" + str(dl_url[0]) + """</a></p>
                    <p>测试所得截图：</p>
                    <p><img src='cid:%s'></p>
                    """ % imgpath
            text = MIMEText(mail_img, 'html', 'utf-8')
            msg.attach(text)
        else:
            mail_img = """
                                <p>此包为之前没有更新成功的包，已无法获取链接</p>
                                <p>测试所得截图：</p>
                                <p><img src='cid:%s'></p>
                                """ % imgpath
            text = MIMEText(mail_img, 'html', 'utf-8')
            msg.attach(text)

        smtp = smtplib.SMTP(email_host, port=25)  # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
        smtp.login(self.username, self.password)  # 发送者的邮箱账号，密码
        smtp.sendmail(self.username, self.receiver.split(','), msg.as_string())
        # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
        smtp.quit()  # 发送完毕后退出smtp
        print('email send success.')


class do_log(object):
    def get_log(self):
        """清空log并重新开始抓取"""
        os.popen("adb logcat -c")
        time.sleep(2)
        print("log开始抓取……")
        subprocess.Popen('adb shell logcat -v time > ' + log_Path + "applog.txt", shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    def stop_log(self):
        """结束logcat进程"""
        log_lines = os.popen("adb shell ps | findstr logcat").readlines()
        for log_line in log_lines:
            if log_line != "\n":
                a = log_line.split(' ')
                while 1:
                    if "" in a:
                        a.remove("")
                    else:
                        break
                os.popen("adb shell kill " + a[1])
        print("log已停止抓取")


class FileOperate(object):
    def del_line(self, txtline):  # 清除文件中某行内容
        with open(link_files_path + "backup.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(link_files_path + "backup.txt", "w", encoding="utf-8") as f_w:
            for line in lines:
                if txtline in line:
                    continue
                f_w.write(line)

    def copy_file(self, srcfile, dstfile):  # 复制文件
        if os.path.exists(srcfile) is False:  #
            print("%s not exist!" % (srcfile))
            return False
        else:
            fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
            if not os.path.exists(fpath):
                os.makedirs(fpath)  # 创建路径
            shutil.copyfile(srcfile, dstfile)  # 复制文件
            print("copy %s -> %s" % (srcfile, dstfile))
            return True

    def get_file_md5(self, filename):
        """ 获取MD5 """
        if not os.path.isfile(filename):
            return
        md5 = hashlib.md5()
        f = open(filename, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            md5.update(b)
        f.close()
        return md5.hexdigest()

    def confirm_md5(self):
        """ 验证新下载的prevercode.txt文件是否和上次下载的MD5一致，如果不一致，则把prevercode.txt的内容
        写入backup.txt内，并把prevercode.txt重命名为lastfile.txt """
        m1 = self.get_file_md5(link_files_path + "lastfile.txt")
        m2 = self.get_file_md5(link_files_path + "prevercode.txt")
        if m1 != m2:
            try:
                for line in open(link_files_path + "prevercode.txt", encoding="utf-8"):
                    with open(link_files_path + 'backup.txt', 'a') as f:
                        f.write("\n" + line)
                os.remove(link_files_path + "lastfile.txt")
                os.rename(link_files_path + "prevercode.txt", link_files_path + "lastfile.txt")
            except:
                pass
            return True
        else:
            try:
                os.remove(link_files_path + "prevercode.txt")
            except FileNotFoundError:
                pass
            return False


class Judgement(object):
    def __get_picture_path(self, apkname):
        img_folder = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        times = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        screen_save_path = img_folder + "\\" + times + "-" + apkname + '.png'
        return screen_save_path

    def get_screenshot(self, save_path):
        cmd1 = r"adb shell screencap -p /sdcard/1.png"
        cmd2 = r"adb pull /sdcard/1.png " + save_path
        cmd3 = r"adb shell rm /sdcard/1.png"
        cmd4 = r"adb shell screencap -p | sed 's/\r$//' > screen.png"
        p = subprocess.Popen(str(cmd1), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        time.sleep(4)
        subprocess.Popen(str(cmd2), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        time.sleep(4)
        subprocess.Popen(str(cmd3), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    def find_setting(self):
        try:
            driver.find_element_by_xpath("//*[@text='设置']").is_displayed()
            return False
        except:
            return True

    def judge_pic(self, status, apkname, *dl_url):
        emails = Emails()
        print("截图中……")
        sc = self.__get_picture_path(apkname)
        self.get_screenshot(sc)
        ishan = compare_img.calc_similar_by_pathshan(sc)

        if ishan > 0.6:
            ss = apkname + "闪退了+" + sc
            print(ss)
            emails.send_email(status + apkname + "闪退了", sc, dl_url[0])
            try:
                shutil.move(apk_dl_Path + apkname, err_apk_path)
            except shutil.Error:
                pass
            print("闪退应用已移至err_app文件夹")
            return False

    def judge_pic2(self, status, apkname, *dl_url):
        """每1s截一次图，共截8次图，如果每一张图均符合异常判断条件，则发送邮件"""
        emails = Emails()
        white_list = []
        black_list = []
        err_list = []
        i = 0
        w_err = 0
        b_err = 0
        err = 0
        print("截图中……")
        while i < 10:
            sc = self.__get_picture_path(apkname)
            driver.get_screenshot_as_file(sc)
            imf = compare_img.calc_similar_by_pathbai(sc)
            white_list.append(round(imf, 4))
            imf2 = compare_img.calc_similar_by_pathhei(sc)
            black_list.append(round(imf2, 4))
            ishan = compare_img.calc_similar_by_pathshan(sc)
            err_list.append(round(ishan, 4))
            time.sleep(1)
            i = i + 1

        print("白屏数据：")
        print(white_list)
        print("黑屏数据：")
        print(black_list)
        print("闪退数据：")
        print(err_list)

        for white in white_list:
            if white > 0.98:
                w_err = w_err + 1
            else:
                pass

        for black in black_list:
            if black > 0.98:
                b_err = b_err + 1
            else:
                pass

        for er in err_list:
            if er > 0.6:
                err = err + 1
            else:
                pass

        if w_err >= 9 or b_err >= 9:
            b = apkname + "白屏时间过长或黑屏时间过长+" + sc
            print(b)
            emails.send_email(status + apkname + "白屏时间过长或黑屏时间过长", sc, dl_url[0])
            try:
                shutil.move(apk_dl_Path + apkname, err_apk_path)
            except shutil.Error:
                pass
            print("白屏或黑屏应用已移至err_app文件夹")
            return False

        if err >= 8 and self.find_setting() is False:
            ss = apkname + "闪退了+" + sc
            print(ss)
            emails.send_email(status + apkname + "闪退了", sc, dl_url[0])
            try:
                shutil.move(apk_dl_Path + apkname, err_apk_path)
            except shutil.Error:
                pass
            print("闪退应用已移至err_app文件夹")
            return False


class MainTest(object):
    def __init__(self):
        emails = Emails()
        fo = FileOperate()
        appium = AppiumInit()
        b = 0
        while b < 15:
            b = b + 1
            while 1:
                self.now_time()
                emails.get_mails()
                cp = fo.copy_file(link_files_path + "prevercode.txt", link_files_path + "backup.txt")
                if cp is False:  # 如果没有附件，则删掉邮件
                    self.now_time()
                    emails.del_mail()
                    print("该邮件无附件，已经删除")
                    time.sleep(10)
                elif os.path.getsize(link_files_path + "prevercode.txt") <= 10:  # 如果有附件但没内容也删掉
                    print("该邮件附件内容为空，已删除")
                    emails.del_mail()
                else:
                    f1 = fo.get_file_md5(link_files_path + "prevercode.txt")
                    f2 = fo.get_file_md5(link_files_path + "lastfile.txt")
                    if f1 != f2:  # 如果新附件和上次获得的附件不一样，则移除lastfile，新附件重命名为lastfile
                        try:
                            os.remove(link_files_path + "lastfile.txt")
                        except FileNotFoundError:
                            pass
                        os.rename(link_files_path + "prevercode.txt", link_files_path + "lastfile.txt")  # 修改名字等下次验证MD5
                        appium.check_appium_server()
                        time.sleep(5)
                        self.check_test()
                    else:
                        try:
                            os.remove(link_files_path + "prevercode.txt")
                            print("下载的prevercode.txt已移除")
                        except:
                            pass
                        print(colored("未获取到新邮件，5分钟后重试", "red"))
                        time.sleep(300)
                        # break

    def file_name(self, file_dir):
        """获取路径下所有文件名"""
        for root, dirs, files in os.walk(file_dir):
            # print(root)  # 当前目录路径
            # print(dirs)  # 当前路径下所有子目录
            return files  # 当前路径下所有非目录子文件

    def present_time(self):
        """返回当前时间，并显示为24小时制的时分"""
        return int(time.strftime('%H%M', time.localtime(time.time())))

    def now_time(self):
        """获取当前时间并输出"""
        get_time = datetime.datetime.now()
        now_time = get_time.strftime('%Y-%m-%d %H:%M:%S')
        print(colored(now_time, "cyan"), end="  ")

    def force_up(self, apkname):
        """杀掉测试包的所有进程"""
        op = os.popen("adb shell ps |find \"" + apkname + "\"")
        oo = op.readlines()
        for i in oo:
            if i != "\n":
                i = i.split(" ")
                os.popen("adb shell kill " + i[2])

    def launch_myapp(self, apk_name, apkpath):
        judge = Judgement()
        getinfo = GetInfo()
        while 1:
            driver.launch_app()
            time.sleep(2)
            fs = judge.find_setting()
            if fs is False:
                os.popen("adb shell am start -n " + apk_name + "/" + getinfo.get_apk_activity(apkpath))
            else:
                break

    def get_install(self, url):
        """传入txt文件中获取的链接地址"""
        fd = FileOperate()
        dl_url = "http://" + url  # 这里网址结尾为.obb
        lu = url.split("/")
        l6 = lu[-1].split("obb")
        a = l6[0]
        apk_name = a + "apk"
        apk_path = apk_dl_Path + apk_name
        print(apk_path)
        print(dl_url)
        apkn = re.search(r'.*_([a-z].*).apk', apk_name)
        print(apkn.group(1))
        try:
            head = requests.head(dl_url)
            s = int(head.headers['Content-Length'])
            size = round(s / (1024 * 1024), 2)
            print("该包大小为：" + str(size) + "M")
            if size >= 1500:
                fd.del_line(url)
                return
            else:
                pass
        except:
            print(colored("未获取到包体大小"), "red")
        self.now_time()
        print("开始下载")
        r = requests.get(dl_url)

        if r.status_code == 200:
            with open(apk_path, "wb") as code:
                code.write(r.content)
                self.now_time()
                print("下载完成")
            fd.del_line(url)
            self.now_time()
            print("安装中...")
            p = subprocess.Popen("adb install " + apk_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = p.communicate()
            oo = ''.join('%s' % id for id in out)
            if "Success" in oo:
                self.now_time()
                print("安装成功")
                self.hot_updata(apk_path, apkn.group(1), apk_name, dl_url)
            else:
                self.now_time()
                print(colored("安装失败" + apk_path, "red"))
        else:
            self.now_time()
            print('aidUrl请求返回错误，错误码为： %d' % r.status_code)
            print(url)
            with open(link_files_path + 'noup.txt', 'a') as f:
                f.write("\n" + url)
            fd.del_line(url)

    def check_test(self):
        emails = Emails()
        fo = FileOperate()
        time1 = self.present_time()
        time2 = 0
        with open(link_files_path + "backup.txt", 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    print(line)
                    self.get_install(line)
                    time2 = abs(self.present_time() - time1)
                    tt = self.present_time() % 100
                    if tt <= 2 or time2 >= 100:
                        time1 = self.present_time()
                        have_em = emails.get_mails()
                        if have_em is not True:  # 判断邮件是否有附件，没有则删掉
                            emails.del_mail()
                        elif os.path.getsize(link_files_path + "prevercode.txt") <= 10:  # 如果有附件但没内容也删掉
                            print("该邮件附件内容为空，已删除")
                            emails.del_mail()
                        else:
                            pass

                        ff = fo.confirm_md5()
                        if ff is True:
                            time.sleep(5)
                            self.check_test()
                        else:
                            pass

        if time2 < 100:
            self.now_time()
            print("热更文件夹下之前没有更新成功的包：")
            failed_up_pkgname = self.file_name(apk_dl_Path)
            time3 = 0
            for fup in failed_up_pkgname:
                print(fup)
                self.now_time()
                print("安装中...")
                p = subprocess.Popen("adb install " + apk_dl_Path + fup, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                out = p.communicate()
                oo = ''.join('%s' % id for id in out)
                apkn = re.search(r'.*_([a-z].*).apk', fup)
                print(apkn.group(1))
                if "Success" in oo:
                    self.now_time()
                    print("安装成功")
                    self.hot_updata(apk_dl_Path + fup, apkn.group(1), fup, "此包为之前没有更新成功的包，已无法获取链接")
                    try:
                        os.remove(apk_dl_Path + fup)
                    except:
                        pass
                    time3 = abs(self.present_time() - time1)
                    if self.present_time() % 100 <= 2 or time3 >= 100:
                        have_em1 = emails.get_mails()
                        if have_em1 is not True:
                            emails.del_mail()
                            time.sleep(1)
                            emails.get_mails()
                        elif os.path.getsize(link_files_path + "prevercode.txt") <= 10:  # 如果有附件但没内容也删掉
                            print("该邮件附件内容为空，已删除")
                            emails.del_mail()
                        else:
                            pass
                        fc = fo.confirm_md5()
                        if fc is False:
                            print("没有新邮件，继续热更遗留的包")
                            pass
                        else:
                            self.check_test()
                            break
                else:
                    self.now_time()
                    print(colored("安装失败", "red"))
                    os.remove(apk_dl_Path + fup)

            while 1:
                print(time3)
                pt = self.present_time()
                print("当前时间：" + str(pt))
                print("测试开始时间：" + str(time1))
                if pt % 100 <= 2 or time3 >= 100:
                    have_em2 = emails.get_mails()
                    if have_em2 is not True:
                        emails.del_mail()
                    elif os.path.getsize(link_files_path + "prevercode.txt") <= 10:  # 如果有附件但没内容也删掉
                        print("该邮件附件内容为空，已删除")
                        emails.del_mail()
                    else:
                        pass
                    fo.confirm_md5()
                    time.sleep(20)
                    self.check_test()
                    break
                else:
                    self.now_time()
                    print("等待中...")
                    time.sleep(120)
                    time3 = abs(self.present_time() - time1)

    def hot_updata(self, apkpath, apkname, v_apkname, *dl_url):
        hot_flag = 0
        times_flag = 0
        ww = 0
        up_ok_flag = 0
        wh = 0
        w = 0

        print(apkpath)
        getinfo = GetInfo()
        judgement = Judgement()
        appium = AppiumInit()
        self.now_time()
        do_log().get_log()
        try:
            print("_" * 32)
            appium.appium_init(apkpath)
        except selenium.common.exceptions.WebDriverException:
            time.sleep(2)
            self.now_time()
            judgement.judge_pic("安装后启动", v_apkname, dl_url[0])
            self.now_time()
            print(colored("应用异常，即将跳过当前应用测试下一应用……", "red"))
            return
        time.sleep(6)
        self.now_time()
        bb = judgement.judge_pic2("安装后首次启动", v_apkname, dl_url[0])
        if bb is False:
            driver.remove_app(apkname)
            return
        apk_name = apkname
        print(apk_name)
        b_time = int(time.time())  # 开始的时间戳
        while 1:
            if hot_flag == 1:
                time.sleep(5)
                while 1:
                    if int(time.time()) - b_time >= 900:  # 如果测试当前包测试时间大于15分钟，则放弃测试此包
                        self.now_time()
                        print(colored("测试时间过长，跳过该应用", "red"))
                        driver.remove_app(apk_name)
                        return
                    else:
                        pass
                    if times_flag % 2 == 0:
                        self.now_time()
                        jde = judgement.judge_pic2("更新过程中", v_apkname, dl_url[0])
                        if jde is False:
                            driver.remove_app(apk_name)
                            return
                    elif times_flag == 15:
                        os.popen("adb shell am force-stop " + apk_name)
                        time.sleep(2)
                        self.launch_myapp(apk_name, apkpath)
                        # driver.launch_app()
                        time.sleep(3)
                    else:
                        pass
                    try:
                        driver.find_element_by_android_uiautomator(
                            'new UiSelector().resourceIdMatches(".*id/lebian_positiveButton$")').click()
                        # driver.find_element_by_id(apk_name + ":id/lebian_positiveButton").click()
                    except:
                        pass
                    try:
                        driver.find_element_by_xpath("//*[@text='下载失败，请检查网络']").is_displayed()
                        self.now_time()
                        print(colored("网络错误，重启应用！", "red"))
                        driver.close_app()
                        time.sleep(2)
                        os.popen("adb shell am start -n " + apk_name + "/" + getinfo.get_apk_activity(apkpath))
                        time.sleep(2)
                    except:
                        pass
                    try:
                        driver.find_element_by_android_uiautomator(
                            'new UiSelector().resourceIdMatches(".*id/lebian_positiveButton$")').click()
                        # driver.find_element_by_id('lebian_positiveButton').click()
                    except:
                        pass

                    apk_pid = getinfo.get_pid(apk_name)
                    if apk_pid is not None:
                        times_flag = times_flag + 1
                        self.now_time()
                        print("获取数字为：" + colored(apk_pid, "cyan"))
                        ca = os.popen("adb shell cat /proc/" + apk_pid + "/maps | find \"lbvmrt.dex\"")
                        i = str(ca.readlines())
                        ca2 = os.popen("adb shell cat /proc/" + apk_pid + "/maps | find \"kxqpplatform.dex\"")
                        i2 = str(ca2.readlines())
                        print(i + "*********" + i2)
                        if "lbvmrt.dex" in i or "kxqpplatform.dex" in i2:
                            self.now_time()
                            print(colored("含有vmdex或者kxqpplatformdex", "green"))
                            up_ok_flag = up_ok_flag + 1
                            wh = 1
                            times_flag = 0
                            time.sleep(1)
                        else:
                            ca = os.popen(
                                "adb shell cat data/data/" + apk_name + "/shared_prefs/excl_lb_gameInfo.xml")
                            i = ca.read()
                            o = "<boolean name=\"downloadFinish\" value=\"true\" />"

                            if o in i:
                                self.now_time()
                                print(colored("检测到downloadFinish值为true，杀进程", "blue"))
                                os.popen("adb shell am force-stop " + apk_name)  # 杀掉包名下的所属id进程
                                time.sleep(2)
                                self.now_time()
                                print(colored("重启应用……", "blue"))
                                self.launch_myapp(apk_name, apkpath)
                                qq = judgement.judge_pic2("检测到downloadFinish值为true，杀进程之后", v_apkname, dl_url[0])
                                if qq is False:
                                    print("重启过程中发现异常")
                                    driver.remove_app(apk_name)
                                    return
                                self.now_time()
                                print(colored("重启成功", "blue"))

                    appium.overlay()
                    fg = appium.overlay_launch()
                    if fg is True:
                        time.sleep(1)
                        self.now_time()
                        judgement.judge_pic2("覆盖安装再启动", v_apkname, dl_url[0])
                    else:
                        pass
                    if wh == 1:
                        break
                    elif times_flag > 15:
                        ww = ww + 1
                        break
                    else:
                        print("开始休眠！")
                        print("time_flag:" + str(times_flag))
                        time.sleep(5)
                        print("休眠完毕！")

                    try:
                        driver.find_element_by_name("安装").click()
                        ww = ww + 1
                        break
                    except BaseException:
                        continue

                if up_ok_flag == 2:
                    self.now_time()
                    print("更新没问题！" + apkname)
                    driver.close_app()  # 关闭app
                    driver.remove_app(apk_name)  # 卸载app
                    try:
                        os.remove(apkpath)
                    except FileNotFoundError:
                        pass
                    break
                elif ww > 0:
                    driver.close_app()  # 关闭app
                    driver.remove_app(apk_name)  # 卸载app
                    os.remove(apkpath)
                    break

            else:
                z = 0
                while 1:
                    time.sleep(1)
                    click_cf = appium.confirm_click()  # 检测更新弹框并点击下载
                    self.now_time()
                    print('confirm_click返回为：' + str(click_cf))

                    ca = os.popen(
                        "adb shell ls /sdcard/Android/obb/" + apk_name + "/lebian/downloading")
                    i = ca.read()
                    ca2 = os.popen(
                        "adb shell ls /sdcard/Android/obb/" + apk_name + "/lebian/" + apk_name + "-1")
                    i2 = ca2.read()
                    if (".cfg" in i and ".dload" in i) or ".odex.jar" in i2 or click_cf == True:
                        hot_flag = 1
                        print(colored("跳转至更新完成检查", "blue"))
                        break
                    else:
                        lss = os.popen("adb shell ls /data/data/" + apk_name + "/lebian/downloading")
                        s = lss.read()
                        l3 = os.popen(
                            "adb shell ls /data/data/" + apk_name + "/lebian/" + apk_name + "-1")
                        s2 = l3.read()
                        if (".cfg" in s and ".dload" in s) or ".odex.jar" in s2:
                            hot_flag = 1
                            print(colored("跳转至更新完成检查", "blue"))
                            break
                        else:
                            w = w + 1
                            os.popen("adb shell am force-stop " + apk_name)
                            time.sleep(3)
                            os.popen(
                                "adb shell am start -n " + apk_name + "/" + getinfo.get_apk_activity(apkpath))  # 启动应用
                            time.sleep(2)
                            z = z + 1
                            rr = str(z)
                            self.now_time()
                            jj = judgement.judge_pic2("第" + rr + "次启动后杀进程再启动", v_apkname, dl_url[0])
                            if jj is False:
                                driver.remove_app(apk_name)
                                return
                            else:
                                pass
                            if w == 3:
                                self.now_time()
                                print("没有更新需求！" + apkname)
                                driver.close_app()
                                time.sleep(1)  # 关闭app
                                self.now_time()
                                print("卸载APP")
                                driver.remove_app(apk_name)  # 卸载app
                                self.now_time()
                                print("卸载完成")
                                # os.remove(apkpath)
                                ww = ww + 1
                                break
            if up_ok_flag == 2 or ww > 0:
                break
        self.now_time()
        do_log().stop_log()
        self.now_time()
        print("退出")
        appium.quit()


if __name__ == "__main__":
    # MainTest().hot_updata(apk_dl_Path+"67633_30_1.1_com.netease.nshhelper.apk", "67633_30_1.1_com.netease.nshhelper.apk","http://cdn.regengxin.com/origapk/otaapk/67633/30/gver1/lvl1/67633_30_1.1_com.netease.nshhelper.obb")
    # Emails().get_mails()
    # Emails().send_email('ceshi', "E:\\TobTest\\com.netease.lx12.bilibili-201807301024.png")
    # do_log().get_log()
    # do_log().stop_log()
    MainTest()
    # MainTest().get_install('cdn.regengxin.com/origapk/otaapk/67756/11/gver5/lvl1/67756_11_5.1_com.yiwan.mssj.obb')
    # GetInfo().get_apk_activity(r"D:\TobTest\apk_dl\66881_59_1.1_com.live91y.tv.apk")
    # MainTest.hot_updata('E:\\TobTest\\apk_dl\\67380_11_1.1_com.xinlian.coinu.apk', "67380_11_1.1_com.xinlian.coinu.apk")
    # appium = AppiumInit()
    # appium.appium_init(apk_dl_Path+'67062_7_2.1_com.yqlmx.yx.m4399.apk')
    # appium.overlay_lauch()
    # appium.confirm_click()
    # driver.close_app()
    # driver.remove_app('com.lixxix.hall.apk')
    # Judgement().find_setting()
