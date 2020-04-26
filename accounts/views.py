from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View

from .forms import RegisterForm, UserEditForm, ProfileEditForm
from .models import Profile


class RegisterView(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
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
        {"user_form": user_form, "profile_form": profile_form})
