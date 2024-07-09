from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

def send(receiverEmail, verifyCode):
    try:
        content = {
            'verifyCode': verifyCode
        }
        
        msg_html = render_to_string('sendEmail/email_format.html', content)
        msg = EmailMessage(subject = "인증 코드 발송 메일입니다.", body = msg_html, from_email = "triojang2@gmail.com",
                           bcc=[receiverEmail]) # 받는 사람이 여러명일 수 있으므로 리스트에 담는다.
        
        msg.content_subtype = 'html'
        msg.send()
        return True    
    except:
        return False
# Create your views here.
