import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class email:
    def __init__(self, sender_email, sender_password, receiver_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email

    def send_email(self, subject, body):
        # 설정
        smtp_server = 'smtp.gmail.com'  # 이용할 이메일 서버 (Gmail의 경우 'smtp.gmail.com'을 사용)
        smtp_port = 587  # SMTP 포트 (Gmail의 경우 587을 사용)

        # 이메일 내용 설정
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = subject

        # 이메일 본문 추가
        msg.attach(MIMEText(body, 'plain'))

        # SMTP 서버 연결 및 이메일 보내기
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # TLS 암호화를 사용하려면 이 부분이 필요합니다.
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            print("이메일이 성공적으로 보내졌습니다.")
        except Exception as e:
            print("이메일 보내기 실패:", e)
        finally:
            server.quit()

# em = email("mintae1134@gmail.com",'gxfiurgrgjptxrhe','mintae3827@naver.com','dkljf', 'dkfjdkfjdkfj')
# em.send_email()