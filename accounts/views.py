import datetime
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings

from .forms import RegisterForm, UserEditForm, ProfileEditForm
from .models import Profile
from .tokens import token_generator


logger = logging.getLogger(__name__)


class RegisterView(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            logger.info('User registered: ' + new_user.username)
            Profile.objects.create(user=new_user)

            return render(request, "accounts/register_complete.html",
                          {"new_user": new_user})

        return render(request, "accounts/register.html", {"user_form": form})

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, "accounts/register.html", {"user_form": form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        "accounts/edit.html",
        {"user_form": user_form,
         "profile_form": profile_form,
         "verified": request.user.profile.verified})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_activate = True
        profile = Profile.objects.get(user=user)
        profile.verified = True
        logger.info('User activated: ' + user.first_name)
        profile.save()
        user.save()
        messages.success(request, f'Спасибо за подверждение регистрации.')
        return redirect('/tasks/list')
    else:
        messages.success(request, f'Неправильная ссылка активации!')
        return redirect('login')


def send(request, user_id):
    if user_id is not None:
        try:
            user = Profile.objects.get(id=user_id).user
            messages.success(request, f'Сообщение отправлено пользователю {user},'
                                      f' email: {user.email}, user id: {user_id}')
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            current_site = get_current_site(request)
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'time': datetime.datetime.now(),
                'domain': current_site,
                'uid': uid,
                'token': token,
            })
            send_mail("Подтвердите регистрацию", "", settings.EMAIL_HOST_USER,
                      [user.email], fail_silently=True, html_message=message)
        except (TypeError, ValueError, IndexError, IndentationError):
            messages.error(request, f'Ошибка при отправке сообщения пользователю с id: {user_id}')

    return redirect('/admin/accounts/profile/')
