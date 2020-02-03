import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# 第三方 SMTP 服务
def mail(mail_host, mail_user, mail_pass, sender, content, title, receivers, file_path=''):
    '''
    :param mail_host: # SMTP服务器
    :param mail_user: # 用户名
    :param mail_pass: # 授权码
    :param sender: # 发件人邮箱
    :param receivers: # 接收人邮箱
    :param content: # 内容
    :param title: # 邮件主题
    :param file_path：# 文件附件路径
    :return: True or error
    '''
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers) if isinstance(receivers, list) else [receivers]
    message['Subject'] = title

    '''
    # 带附件的邮件
    # 创建MIMEApplication的对象
    # 注意：发送文件，实际上发送的是二进制文件
    # 参数：需要被发送的文件对象的内容
    '''

    if file_path != '' and os.path.isfile(file_path):
        # part = MIMEApplication(open(f"{file_path}", "rb").read())
        # # 设置配置信息[添加头文件]
        # part.add_header("Content-Disposition", "attachment", filename=f"{os.path.split(file_path)[1]}")
        # message.attach(part)

        # 添加report附件
        att = MIMEText(open(f"{file_path}", "rb").read(), "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        times = time.strftime("%m_%d_%H_%M", time.localtime(time.time()))
        filename_report = 'FM_Android_Report' + '_' + times + '.zip'
        att["Content-Disposition"] = 'attachment; filename= %s ' % filename_report
        message.attach(att)
    else:
        # return type('FileError', (OSError,), {'error':'附件错误'})
        return '附件错误'
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        return True
    except smtplib.SMTPException as e:
        return e


if __name__ == '__main__':
    mail_host = "smtp.126.com"
    mail_user = "qq8699705"
    mail_pass = "qq1100126"
    sender = 'qq8699705@126.com'
    receivers = ['2689392709@qq.com']
    content = '这个是文件内容'
    title = 'Python SMTP 插件'
    file_path = r'C:\Users\骆江尚\Desktop\新建文件夹\aaa.png'

    print(mail(mail_host=mail_host, mail_user=mail_user, mail_pass=mail_pass, sender=sender,
         receivers=receivers, content=content, title=title, file_path=file_path))
