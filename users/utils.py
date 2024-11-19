import os
import uuid
import random
import hashlib
import requests
from .models import User
from functools import partial
from main.models import Profile
from django.conf import settings
from datetime import datetime, timedelta
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from utils import generate_media_path, generate_uuid
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class OTP:
    def __init__(self):
        self.otp = "-1"

    def generateOTP(self):
        _otp = random.randint(100000, 999999)
        while self.otp == _otp:
            _otp = random.randint(100000, 999999)

        self.otp = _otp
        return {"otp": str(_otp), "ttl": str(datetime.now() + timedelta(minutes=2))}

    @staticmethod
    def verifyOTP(otp: str, user_otp: str):
        return otp == user_otp

    @staticmethod
    def getCurrentTime():
        return str(datetime.now())


OTPTools = OTP()


class Encryption:
    def __init__(self):
        self.salt = os.urandom(32)

    def getHash(self, value: str):
        return hashlib.pbkdf2_hmac(
            "sha256", value.encode("utf-8"), self.salt, 100000
        ).hex()

    @staticmethod
    def generateToken(remote_addr: str, local_username: str, device_name: str):
        data = f"{remote_addr}-{local_username}-{device_name}"
        print(data)
        return uuid.uuid5(
            namespace=uuid.NAMESPACE_URL,
            name=data,
        ).hex


EncryptTools = Encryption()


def sendEmail(user, otp, reset_password=False, register_cofirm=False):
    if reset_password:
        subject = "Reset Password - Tell Your Friends"
        context = "reset your password"
    elif register_cofirm:
        subject = "Confirm Registration - Tell Your Friends"
        context = "confirm registration"
    else:
        return

    html_content = render_to_string(
        "main/email_template.html", {"context": context, "otp_key": otp}
    )

    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def create_profile(user, is_new=False, *args, **kwargs):
    if is_new:
        try:
            email = kwargs["details"]["email"] or ""
            username = kwargs["details"]["username"] or ""
            first_name = kwargs["details"]["first_name"] or ""
            last_name = kwargs["details"]["last_name"] or ""

            user_profile = Profile.objects.get(email=email)
            if username != "":
                user_profile.username = username
            if first_name != "":
                user_profile.first_name = first_name
            if last_name != "":
                user_profile.last_name = last_name
            user_profile.save()

        except:
            pass


AccountActivationToken = PasswordResetTokenGenerator()
