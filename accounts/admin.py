from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import format_html
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
import datetime
from multiprocessing import Pool

from .models import Profile
from .tokens import token_generator


def send(selected_user):
    user = selected_user.user
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'time': datetime.datetime.now(),
        'domain': 'http://localhost:8000',
        'uid': uid,
        'token': token,
    })
    send_mail("Confirm your registration", "", settings.EMAIL_HOST_USER,
              [user.email], html_message=message)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "birth_date", "verified", "avatar", "send_email_button"]
    actions = ['send_email']

    def send_email_button(self, obj):
        return format_html('<a class="btn-default" href="/send/{}/">Send</a>', obj.id)

    send_email_button.allow_tags = True

    def send_email(self, request, queryset):
        if queryset:
            recipients = [user for user in queryset]
            pool = Pool(processes=5)
            pool.map_async(send, recipients)

    send_email.short_description = "Send validation email"
