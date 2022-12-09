import os
import random
import re
import json
import smtplib
import wmi
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

HASH_MD5 = hashlib.md5()
VerCode = str(random.randint(10000, 99999))

getBaseBoard_Win = wmi.WMI()


def getBaseBoard():
    baseboard = []
    for board_id in getBaseBoard_Win.Win32_BaseBoard():
        baseboard.append(board_id.SerialNumber.strip().strip('.'))
        get_BaseBoard = ''.join(baseboard)
    return get_BaseBoard


Baseboard_win = getBaseBoard()


def Sign_up(Vali_Email, SMTP_License_Code):
    os.system("cls")

    with open("./Account.json", "r") as f:
        Json_Account = json.load(f)

    if Baseboard_win == Json_Account["Baseboard"]:
        print("您已经注册过了")
        return False

    print("欢迎注册")
    UserName = input("用户名:")

    UserName_ENCODE = UserName.encode("UTF-8")
    HASH_MD5.update(UserName_ENCODE)
    UserName_HASHED = HASH_MD5.hexdigest()

    UserPassWord = input("密码(长度不可小于或等于6):")

    UserPassWord_Len = len(UserPassWord)
    if UserPassWord_Len <= 7:
        print("密码长度小于或等于6, 请重试")
        return False

    UserPassWord = UserPassWord.encode("UTF-8")
    HASH_MD5.update(UserPassWord)
    UserPassWord_HASHED = HASH_MD5.hexdigest()

    UserEmail = input("邮箱:")

    pattern = re.compile(r"[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)")

    Validation = pattern.findall(UserEmail)
    ValidationEd = ''.join(Validation)
    Contrast = UserEmail == ValidationEd

    if not Contrast:
        print("邮箱格式不正确, 请重试")
        os.system("pause")
        return False
    else:
        pass

    fromaddr = Vali_Email  # 发送方邮箱
    password = SMTP_License_Code  # 开启邮箱 SMTP 服务后获取的授权码
    toaddrs = [UserEmail]  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    content = '正文内容：Dome验证码:' + VerCode + "\n" + "账号名称为:" + UserName + ", 如果不是您主动注册该软件, 请您忽视此邮件"
    textApart = MIMEText(content)
    m = MIMEMultipart()
    m.attach(textApart)  # 文本
    # m.attach(imageApart)  # 发送图片附件
    m['Subject'] = '主题：Dome验证码'
    m['From'] = "验证码"

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)  # 连接QQ邮箱的smtp服务器，和对应端口
        server.login(fromaddr, password)  # 登入你的账号
        server.sendmail(fromaddr, toaddrs, m.as_string())  # 从谁发送给谁，内容是什么
        server.quit()
    except smtplib.SMTPException as e:
        print('error:', e)  # 打印错误
    print("100 % |█████████████████████████ | 1 / 1")
    print("验证码已发送至您的邮箱,请及时查收.如果没看到验证码,请去广告邮件一栏看看或者等一等,可能发的有点慢")
    VerCode_Input = input("验证码:")
    if VerCode_Input != VerCode:
        print("验证码错误, 请重新输入")
    else:
        print("验证码正确")
    os.system("pause")
    os.system("cls")

    DICT_INFO = {
        "UserName"    : UserName_HASHED,
        "UserPassWord": UserPassWord_HASHED,
        "UserEmail"   : UserEmail,
        "Baseboard"   : getBaseBoard(),
    }

    with open("./Account.json", "w") as f:
        json.dump(DICT_INFO, f, indent=4)


def Login():
    if os.path.exists('Account.json'):
        with open("./Account.json", "r") as f:
            Json_Account = json.load(f)
    else:
        with open("Account.json", mode='w', encoding='utf-8') as ff:
            with open("./Account.json", "w") as f:
                Json_Account = json.load(f)
    os.system("cls")
    print("欢迎登录")
    UserName_Login = input("用户名:")
    UserPassWord_Login = input("密码:")
    UserEmail_Login = input("邮箱:")

    UserName_Login = UserName_Login.encode("UTF-8")
    HASH_MD5.update(UserName_Login)
    UserName_Login_HASHED = HASH_MD5.hexdigest()
    if UserName_Login_HASHED != Json_Account["UserName"]:
        print("用户名不正确, 请重新登录")
        return False

    UserPassWord_Login = UserPassWord_Login.encode("UTF-8")
    HASH_MD5.update(UserPassWord_Login)
    UserPassWord_Login_HASHED = HASH_MD5.hexdigest()
    if UserPassWord_Login_HASHED != Json_Account["UserPassWord"]:
        print("用户密码不正确, 请重新登录")
        return False

    if UserEmail_Login != Json_Account["UserEmail"]:
        print("用户邮箱不正确, 请重新登录")
        return False

    print("登录成功")
    os.system("cls")


if __name__ == '__main__':
    Select = input("1.注册\n2.登陆\n")

    if Select == "1" or Select == "注册":
        Sign_up("YourEmail", "SMTP_Code")
        '''
        中文:
        Vali_Email: 填你自己的邮箱，它将被用来发送验证码
        SMTP_License_Code:由于有些邮箱需要激活SMTP来发送邮件，如果你的邮箱也需要SMTP，那就填上，如果不需要，请自行重写代码。

        English:
         Vali_Email: Fill in an email address of your own, which will be used to send the verification code
        
         SMTP_License_Code: Since some mailboxes need to activate SMTP to send emails,
         if your mailbox also needs SMTP, then fill it in,
         if not, please rewrite the code by yourself.
        '''

    elif Select == "2" or Select == "登陆":
        Login()

    else:
        print("您的输入有问题, 请重试")
        exit()
