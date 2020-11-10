from pathlib import Path
import base64
import click
import errno
import json
import os


class AuthService:

    path = os.path.abspath(__file__)
    auth_file = os.path.dirname(path) + '/auth_file.json'
    decoded_data = {}

    def __init__(self, credentials) -> None:
        if credentials or not Path(self.auth_file).is_file():
            self.prompt_auth_data()

        self.create_auth_data()

    def get_user_name(self):
        return self.decoded_data['username']

    def get_password(self):
        return self.decoded_data['password']

    def get_graduation(self):
        return self.decoded_data['graduation']

    def get_subject(self):
        return self.decoded_data['subject']

    def prompt_auth_data(self):
        try:
            if click.confirm(' Wollen Sie die Anmeldedaten eingeben?', abort=True):
                username = click.prompt(' Benutzername')
                password = click.prompt(' Passwort', hide_input=True)
                subject = click.prompt(' Studiengang (Infomatik, Wirtschaftsinformatik, Praktische Informatik,...)')
                graduation = click.prompt(' Abschluss (Bachelor, Master)')
                data = {
                    'username': str(base64.b64encode(bytes(username, 'UTF-8')), 'UTF-8'),
                    'password': str(base64.b64encode(bytes(password, 'UTF-8')), 'UTF-8'),
                    'graduation': graduation,
                    'subject': subject
                }

                with open(self.auth_file, 'w') as outfile:
                    json.dump(data, outfile)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    def create_auth_data(self):
        try:
            with open(self.auth_file) as creds:
                data = json.load(creds)
                user_name = str(base64.b64decode(data['username']), 'UTF-8')
                password = str(base64.b64decode(data['password']), 'UTF-8')
                graduation = f'{data["graduation"]}'
                subject = f'{data["subject"]}'

                self.decoded_data = {
                    'username': user_name,
                    'password': password,
                    'graduation': graduation,
                    'subject': subject
                }
        except OSError as exco:
            if exco.errno != errno.EEXIST:
                raise
