import datetime
from email.message import EmailMessage
import os
import pickle
import random
import string
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from base64 import urlsafe_b64encode


import jwt
from models.user_login_model import UserLoginModel
from requests import HTTPError
import os

SCOPES = ['https://mail.google.com/']
GMAIL = str(os.getenv('GMAIL'))
secret_key = str(os.getenv('SECRET_KEY'))
path = str(os.getenv('CREDENTIALS_PATH'))


def gmail_authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


class EmailVerification:
    """
    Email verification class\n 
    This class is used to send email verification to user

    Args:
        user_email (str): user email
        user (UserLoginModel): user model
    """

    def __init__(self, user_email: str, user: UserLoginModel) -> None:
        self.service = gmail_authenticate()
        self.email = user_email
        self.user_id = str(user.uid)
        user.confirmationTokenExpiration = datetime.datetime.utcnow() + \
            datetime.timedelta(minutes=10)
        self.exp = user.confirmationTokenExpiration
        self.token = self.token_generator()
        user.confirmationToken = self.token
        user.save()
    # for authentication with gmail need to install Gmail API credentials and paste the content to your credentials.json file

    def token_generator(self, length: int = 18) -> str:
        """
        Generates a JSON Web Token that contains the user's id , email and expiration date
        Args:
            length (int, optional): length of the token. Defaults to 18.
        Returns:
            str: token
        """
        token_path = ''.join(random.choices(
            string.ascii_letters + string.digits + self.email, k=length))
        jwt_token = jwt.encode({"token": token_path, "user_id": self.user_id, "exp": self.exp}, str(
            secret_key), algorithm="HS256")
        return jwt_token

    def send(self) -> None:
        """
        sends email verification to user
        """
        try:
            message = EmailMessage()
            message.set_content('Lunaria verification mail')
            message['to'] = self.email
            message['from'] = GMAIL
            message['subject'] = 'Lunaria verification mail'
            message.add_alternative(f'''
                                    <html>
                                        <body>
                                            <h1>Verify your email</h1>
                                            <p>Click the link below to verify your email</p>
                                            <a href="http://localhost:8000/auth/verify/{{email-token}}?email_token={self.token}">Verify</a>
                                        </body>
                                    </html>
                                ''', subtype='html')

            encoded_message = urlsafe_b64encode(message.as_bytes())

            created_message = {
                'raw': encoded_message.decode()
            }
            self.service.users().messages().send(userId='me',
                                                 body=created_message).execute()
        except HTTPError as error:
            print(F'An error occurred: {error}')

#usage
#EmailVerification('whitebirdsdk@gmail.com', 'token').send()
