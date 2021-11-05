from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user
from . import models


def must_be_unique(value):
    user_objects = auth_user.objects.filter(email=value)
    if len(user_objects) > 0:
        raise forms.ValidationError("Email already exists")
    return value 

class GroupForm(forms.Form):
    group_Name = forms.CharField(label='Your Group name', max_length=100)
    group_image = forms.ImageField(
        label="Image File",
        required=False
    )

    def saveGroup(self, request):
        print("request user email ",request.user.email)
        group_instance = models.groupModel()
        group_instance.groupName = self.cleaned_data["group_Name"]
        group_instance.groupAdmin = request.user
        group_instance.save()
        # user_objects = models.userModel.objects.filter(userEmail=request.user.email)
        # print(user_objects[0])
        group_instance.groupUsers.add(request.user)
        return group_instance
    # group_image_description = forms.CharField(
    #     label="Image Description",
    #     max_length=240,
    #     required=False
    # )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    class Meta:
        model = auth_user
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )

    def registerUser(self, commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # user_instance = models.userModel()
            # user_instance.userName = self.cleaned_data["username"]
            # user_instance.userEmail = self.cleaned_data["email"]
            # user_instance.save()
        return user