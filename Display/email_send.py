from random import Random  # 用于生成随机码

from django.core.mail import send_mail  # 发送邮件模块

from QRTree.settings import EMAIL_FROM  # setting.py添加的的配置信息


# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def sendEmail(email, send_type="register"):
    code = random_str(16)
    email_title = send_type
    email_body = "您的验证码为：" + code
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if (send_status):
        print("发送成功")
    else:
        print(send_status)
    return code
