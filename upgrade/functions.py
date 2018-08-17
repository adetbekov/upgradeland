from transliterate import translit, get_available_language_codes
import random, requests
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

def randhash(l):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    upperalphabet = alphabet.upper()
    pwlist = []
    for i in range(l//3):
        pwlist.append(alphabet[random.randrange(len(alphabet))])
        pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
        pwlist.append(str(random.randrange(10)))
    for i in range(l-len(pwlist)):
        pwlist.append(alphabet[random.randrange(len(alphabet))])
    random.shuffle(pwlist)
    return "".join(pwlist)

def rutoen(s):
    return translit(str(s), 'ru', reversed=True)

def strnormalize(s):
    string = ""
    normalstring = "abcdefghijklmnopqrstuvwxyz0123456789_."
    for c in str(s).lower():
        string += "" if (c not in normalstring) else c 
    return string

def send_email(user,hash,template,subject):
    htmly = get_template(template)
    d = Context({ 
        'username': str(user.username),
        'name' : str(user.first_name),
        'hash' : hash
        })
    html_content = htmly.render(d)
    return requests.post(
        "https://api.mailgun.net/v3/portal.tggroup.kz/messages",
        auth=("api", "key-abaa952d6eb9e3680d396982d31486e7"),
        data={"from": "Upgrade Land <no-reply@upgrade-land.kz>",
              "to": user.email,
              "subject": subject,
              "html": html_content
              })

def send_confirm_message(user,hash):
    send_email(user,hash,"invite.html","Активация аккаунта в Upgrade Land")

def send_reset_message(user,hash):
    send_email(user,hash,"restore.html","Восстановление пароля в Upgrade Land")

