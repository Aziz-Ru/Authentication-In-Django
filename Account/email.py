
def send_otp_email(email):
    subject='Your Account Verification Email in BOYS'
    
    message=f'Your verification otp is {otp}'
    email_from=settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj=User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()