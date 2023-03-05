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
mail_receivers = ["dong_qiang819@163.com"]

mm = MIMEMultipart('related')

subject_content = """beng3"""
mm["From"] = "Li Zhejun<lzjgnh2002@gmail.com>"
mm['To'] = "receiver_3_name<dong_qiang819@163.com>"
mm['Subject'] = Header(subject_content, 'utf-8')

body_content = """47698"""
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
