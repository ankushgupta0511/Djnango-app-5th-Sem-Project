from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_email(data):
        
        print('\nemailMessage\n')
        email = EmailMessage(
            subject=data['subject'],   # Take subject From data
            body=data['body'],
            from_email = os.environ.get('EMAIL_FROM'),
            to = [data['to_email']],
        )
        print(email.subject,email.body,email.from_email,email.to)
        print('\nemailMessage\n')
        # email.send()
        
         
        try:
            print('Email sent successfully.!!!!!')
            email.send()
            print('Email sent successfully.!!!!yes')
        except Exception as e:
            print(f'Error sending email: {e}')