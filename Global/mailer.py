import yagmail
import json

CONFIG = json.load(open("../Configs/secret.json"))
EMAIL = CONFIG["BOT_EMAIL"]["EMAIL_ADDRESS"]
PASSWORD = CONFIG["BOT_EMAIL"]["PASSWORD"]

yag = yagmail.SMTP(EMAIL, PASSWORD)


def send_mail(emails, content):
    '''

    :param emails: List of email addresses to send to
    :param contents:
    :return:
    '''
    for email in emails:
        yag.send(to=email, subject='Daily Overview', contents=content)


