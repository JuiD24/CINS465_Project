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
        group_instance.groupImage = self.cleaned_data["group_image"]
        group_instance.save()
        # user_objects = models.userModel.objects.filter(userEmail=request.user.email)
        # print(user_objects[0])
        group_instance.groupUsers.add(request.user)
        return group_instance

ACTIVITY_CHOICES=[ ('Push Ups', 'Push Ups'),
    ('Sit Ups', 'Sit Ups'),
    ('Jumping jacks', 'Jumping jacks'),
    ('star jacks', 'Star jacks'),
    ('skipping', 'Skipping'),
    ('crunches', 'Crunches'),
    ('Mountain Climbers', 'Mountain Climbers'),
    ('Weight Lifting', 'Weight Lifting'),]

SETS_CHOICES = [('15 x 1', '15 x 1 sets'), ('15 x 2', '15 x 2 sets'), ('15 x 3', '15 x 3 sets'),
                ('20 x 1', '20 x 1 sets'), ('20 x 2', '20 x 2 sets'), ('20 x 3', '20 x 3 sets')]    

class ActivityForm(forms.Form):
    activityName = forms.CharField(label="Activity Name", widget=forms.Select(choices=ACTIVITY_CHOICES))
    number_of_sets = forms.CharField(label="Number of sets", widget=forms.Select(choices=SETS_CHOICES))

    def saveActivity(self,request, group_ID):
        groupModel_instance = models.groupModel.objects.get(id=group_ID)
        activity_instance = models.activityModel()
        activity_instance.group = groupModel_instance
        activity_instance.activity_name = self.cleaned_data["activityName"]
        activity_instance.number_of_sets = self.cleaned_data["number_of_sets"]
        activity_instance.addedBy = request.user
        activity_instance.save()
        return activity_instance


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