import email
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
###############################################################################################################################################################
"""email part sending"""
mail_host = "smtp.gmail.com"
mail_sender = "lzjgnh2002@gmail.com"
mail_license = "zbdnlsqoqrlveppn"
mail_receivers = ["1220047112@qq.com", "lzjgnh2002@gmail.com", "dong_qiang819@163.com"]

mm = MIMEMultipart('related')

subject_content = """Python 邮件测试"""
mm["From"] = "Li Zhejun<lzjgnh2002@gmail.com>"
mm['To'] = "receiver_1_name<1220047112@qq.com>,receiver_2_name<lzjgnh2002@gmail.com>,receiver_3_name<dong_qiang819@163.com>"
mm['Subject'] = Header(subject_content, 'utf-8')

body_content = """this is a testing mail这个邮件是为了测试python自动发送邮件功能
附件是一个没用的实验数据"""
message_text = MIMEText(body_content, "plain", "utf-8")
mm.attach(message_text)

file = MIMEText(open('T85I1.dat', 'rb').read(), 'base64', 'utf-8')
file["Content-Disposition"] = 'attachment; filename="T85I1.dat"'
mm.attach(file)

stp = smtplib.SMTP_SSL(mail_host)

stp.set_debuglevel(1)
stp.login(mail_sender, mail_license)
stp.sendmail(mail_sender, mail_receivers, mm.as_string())
print("Email sent Successful!")
stp.quit()
