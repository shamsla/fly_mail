##########################################################

#              Programmer: ShAms LA
#              GitHub: https://github.com/shams-la
#              Email: contact.shams.in@gmail.com

##########################################################


import smtplib

GETBOOL = False


def getDomain(email):
    email = email[email.find("@")+1:email.find(".")]
    return email


def checkDomain(domain):
    if domain == "gmail":
        return "smtp.gmail.com"
    elif domain == "yahoo":
        return "smtp.mail.yahoo.com"
    elif domain in ("outlook", "hotmail"):
        return "smtp-mail.outlook.com"
    else:
        return False


def login(email, password):
    global GETBOOL
    service_provider = checkDomain(getDomain(email))
    if service_provider:
        try:
            connect = smtplib.SMTP(service_provider, 587)
            connect.ehlo()
            connect.starttls()
            connect.login(email, password)
            GETBOOL = True
        except Exception as ex:
            GETBOOL = ex.__class__.__name__


def sendMail(sender, password, reciever, message, subject):
    global GETBOOL
    try:
        connect = smtplib.SMTP(checkDomain(getDomain(sender)), 587)
        connect.ehlo()
        connect.starttls()
        connect.login(sender, password)
        connect.sendmail(sender, reciever,
                         (f"subject: {subject}\n\n{message}"))
        connect.quit()
        GETBOOL = True
    except Exception as ex:
        GETBOOL = ex.__class__.__name__
