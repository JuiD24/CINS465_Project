from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from datetime import datetime, time, timezone
from . import forms
from . import models
from django.contrib.auth.models import User as auth_user


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    context = {
        "title": "Gym Buddy",
        "body" : "Find my Gym Buddy"
    }
    return render(request,"index.html", context=context)

def showGroups(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    context = {
        "title": "Gym Buddy",
        "body" : "Your Groups",
    }
    return render(request,"showGroups.html", context=context)

def createGroup(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    if request.method == "POST":
        form = forms.GroupForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            form.saveGroup(request)
            return redirect("/")
    else:
        form = forms.GroupForm()
    context = {
        "title": "Gym Buddy",
        "body": "Create Group Page",
        "form" : form
    }    
    return render(request,"createGroup.html", context=context)    

def joinGroup(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    context = {
        "title": "Gym Buddy",
        "body" : "Join Groups",
    }
    return render(request,"joinGroups.html", context=context)

def joinGroupList(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    objects = models.groupModel.objects.exclude(groupUsers= (request.user))
    groupDict = {}
    groupDict["groupLists"] = []
    for groupObj in objects:
        reqObj = models.requestModel.objects.filter(group = groupObj).filter(requested_User = request.user)
        if len(reqObj) == 0:
            temp_group = {}
            temp_group["groupName"] = groupObj.groupName
            temp_group["groupID"] = groupObj.id
            temp_group["groupAdmin"] = groupObj.groupAdmin.username
            temp_group["groupAdminID"] = groupObj.groupAdmin.id 
            if groupObj.groupImage:
                temp_group["image"] = groupObj.groupImage.url
            else:
                temp_group["image"] = ""
            time_diff = datetime.now(timezone.utc) - groupObj.added_on
            time_diff_s = time_diff.total_seconds()
            if time_diff_s < 60:
                temp_group["date"] = str(int(time_diff_s)) + " seconds ago"
            else:
                time_diff_m = divmod(time_diff_s,60)[0]
                if time_diff_m < 60:
                    temp_group["date"] = str(int(time_diff_m)) + " minutes ago"
                else:
                    time_diff_h = divmod(time_diff_m,60)[0]
                    if time_diff_h < 24:
                        temp_group["date"] = str(int(time_diff_h)) + " hours ago"
                    else:    
                        temp_group["date"] = groupObj.added_on.strftime("%Y-%m-%d")    
            groupDict["groupLists"] += [temp_group]
    return JsonResponse(groupDict) 

def groupList_view(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    groupobjects = models.groupModel.objects.filter(groupUsers = request.user)
    groupDict = {}
    groupDict["groupLists"] = []
    for groupObj in groupobjects:
        temp_group = {}
        temp_group["groupName"] = groupObj.groupName
        temp_group["group_id"] = groupObj.id
        temp_group["groupAdmin"] = groupObj.groupAdmin.username
        if groupObj.groupImage:
            temp_group["image"] = groupObj.groupImage.url
        else:
            temp_group["image"] = ""
        time_diff = datetime.now(timezone.utc) - groupObj.added_on
        time_diff_s = time_diff.total_seconds()
        if time_diff_s < 60:
            temp_group["date"] = str(int(time_diff_s)) + " seconds ago"
        else:
            time_diff_m = divmod(time_diff_s,60)[0]
            if time_diff_m < 60:
                temp_group["date"] = str(int(time_diff_m)) + " minutes ago"
            else:
                time_diff_h = divmod(time_diff_m,60)[0]
                if time_diff_h < 24:
                    temp_group["date"] = str(int(time_diff_h)) + " hours ago"
                else:    
                    temp_group["date"] = groupObj.added_on.strftime("%Y-%m-%d")    
        groupDict["groupLists"] += [temp_group]
    return JsonResponse(groupDict) 

def request_view(request, group_ID, groupAdmin_ID):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    groupModel_instance = models.groupModel.objects.get(id=group_ID)
    user_instance = models.auth_user.objects.get(id =groupAdmin_ID)
    request_instance = models.requestModel()
    request_instance.group = groupModel_instance
    request_instance.group_Admin = user_instance
    request_instance.requested_User = request.user
    request_instance.save()
    context = {
        "title": "Gym Buddy",
        "body" : "Join Groups",
    }
    return render(request,"joinGroups.html", context=context)

def request_page_view(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    request_from_other_users = models.requestModel.objects.filter(group_Admin=request.user)
    request_to_join_other_groups = models.requestModel.objects.filter(requested_User = request.user)
    context = {
        "title": "Gym Buddy",
        "body":"Your Request",
        "request_from_other_users_list": request_from_other_users,
        "request_to_join_other_groups" : request_to_join_other_groups,
    }
    return render(request,"showRequest.html", context=context) 

def acceptRequest_view(request, req_ID):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    request_obj = models.requestModel.objects.get(id = req_ID)
    request_obj.is_approved = True
    request_obj.group.groupUsers.add(request_obj.requested_User)
    request_obj.save()
    req_group = request_obj.group
    activityObjects = models.activityModel.objects.filter(group = req_group)
    for activity in activityObjects:
        userActivity_instance = models.userActivityModel()
        userActivity_instance.user = request_obj.requested_User
        userActivity_instance.activity = activity
        userActivity_instance.save()
    return redirect("/requestPage/")

def declineRequest_view(request, req_ID):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    request_obj = models.requestModel.objects.get(id = req_ID)
    request_obj.delete()
    return redirect("/requestPage/")

def totalRequest_view(request):
    requestDict = {}
    totalRequest =0
    request_from_other_users = models.requestModel.objects.filter(group_Admin=request.user)
    for req in request_from_other_users:
        if req.is_approved == False:
            totalRequest+=1
    requestDict["totalRequest"] = totalRequest
    return JsonResponse(requestDict) 

def showActivity_view(request, group_ID):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    groupModel_instance = models.groupModel.objects.get(id=group_ID)
    gymbuddyList=[]
    gymbuddy_list = groupModel_instance.groupUsers.all()
    for buddy in gymbuddy_list:
        if buddy != request.user:
            gymbuddyList.append(buddy)
    present = datetime.now(timezone.utc)
    activity_objects = models.activityModel.objects.filter(group = groupModel_instance)
    activity_list=[]
    for activity in activity_objects:
        if(activity.activity_added_on.date() == present.date()):
            activity_list.append(activity)

    context = {
        "title": "Gym Buddy",
        "body": groupModel_instance.groupName + "'s Activities",
        "group_id": group_ID,
        "activity_list" : activity_list,
        "gymbuddy_list" : gymbuddyList,
    }
    return render(request,"showActivity.html", context=context) 

def addActivity_view(request, group_ID):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    if request.method == "POST":
        form = forms.ActivityForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.saveActivity(request, group_ID)
            return redirect("/showActivity/"+str(group_ID)+"/")
    else:
        form = forms.ActivityForm()
    context = {
        "title": "Gym Buddy",
        "body":"Add Activities",
        "form" : form,
        "group_id" : group_ID
    }
    return render(request,"addActivity.html", context=context) 

def deleteActivity_view(request, activity_ID):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    activity = models.activityModel.objects.get(id = activity_ID)
    groupId = activity.group.id
    activity.delete()
    return redirect("/showActivity/"+str(groupId)+"/")

def updateActivity_view(request, activity_ID):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    if request.method == "POST":
        activity = models.activityModel.objects.get(id = activity_ID)
        activity.activity_name = request.POST["activityName"]
        activity.number_of_sets = request.POST["number_of_sets"]
        activity.addedBy = request.user
        activity.save()
        groupId = activity.group.id
        return redirect("/showActivity/"+str(groupId)+"/")
    else:
        form = forms.ActivityForm()
    context = {
        "title": "Gym Buddy",
        "body":"Edit Activities",
        "form" : form,
        "activity_ID":activity_ID
    }
    return render(request,"editActivity.html", context=context) 

def schedule_view(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    userActivity = models.userActivityModel.objects.filter(user = request.user)
    activityList=[]
    present = datetime.now(timezone.utc)
    ActivityNotDone=0
    progress=0
    len_activity = 0
    if userActivity:
        for userActivity_instance in userActivity:
            if(userActivity_instance.activity.activity_added_on.date() == present.date()):
                len_activity += 1
                if userActivity_instance.is_completed == False:
                    ActivityNotDone+=1
                    activityList.append(userActivity_instance.activity)
        if len_activity:
            progress = ((len_activity - ActivityNotDone)/len_activity)*100
    context = {
        "title": "Gym Buddy",
        "body":"Today's Schedule",
        "activityList" : activityList,
        "progress" : int(progress),
    }
    return render(request,"showSchedule.html", context=context) 

def markCompleted_view(request, activity_ID):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    activity = models.activityModel.objects.get(id = activity_ID)    
    userActivity = models.userActivityModel.objects.filter(user = request.user).filter(activity=activity)
    for uActivity in userActivity:
        uActivity.is_completed = True
        uActivity.save()
    return redirect("/showSchedule/")

def chat_view(request, room_name):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    groupobjects = models.groupModel.objects.filter(groupUsers = request.user).filter(id=room_name)
    if groupobjects:
        context ={
            "room_name" : room_name
        }
        return render(request,"chatroom.html", context=context)
    else:
        return redirect("/")

def register_view(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.registerUser(request)   
            return redirect("/login/")
    else:    
        form = forms.RegistrationForm()
    context = {
        "title": "CSU Chico Registration Page",
        "form" : form
    }    
    return render(request,"registration/register.html", context=context)

def logout_view(request):
    logout(request)
    return redirect("/login/")