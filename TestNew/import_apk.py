import os
import re

#pull包到电脑


def import_apk(name):
    package = os.popen("adb shell pm list packages -f " + name).read()
    Gpath = re.search(r'(/\S+\.apk)', package)
    path = Gpath.group(1)
    print(path)
    b = os.popen("adb pull " + path + " C:/Users/zm01/Desktop")
    apk = b.read()


if __name__ == "__main__":
    name = input("package name:")
    import_apk(name)
