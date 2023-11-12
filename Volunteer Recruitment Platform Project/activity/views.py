from django.shortcuts import render, redirect
from .forms import ActivityForm
from .models import Activity
from myapp.models import Administrator
import random
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

def index(request):
    pass
    return render(request, 'activity/index.html')

def showActivity(request):
    template_name = 'activity/activityList.html'
    # context = {'activityList': Activity.objects.all()}
    context = {'activityList': Activity.objects.filter(Q(av_endtime__gt=timezone.now()))}
    return render(request, template_name, context)


def postActivity(request):
    activity_form = ActivityForm()

    if request.method == "POST":
        activity_form = ActivityForm(request.POST)
        print(activity_form.is_valid())
        errors = activity_form.errors.as_data()
        for field, error_list in errors.items():
            for error in error_list:
                print(f"{field}: {error}")

        if activity_form.is_valid():  # 获取数据
            new_id = str(random.randint(0, 999999999))
            old_id_list = Activity.objects.values_list("av_id")
            while new_id in old_id_list:
                new_id = str(random.randint(0, 999999999))

            admin = Administrator.objects.filter(a_id=request.session['user_id']).first()

            activity_type = activity_form.cleaned_data['activity_type']
            activity_state = 1
            group = activity_form.cleaned_data['group']
            location = activity_form.cleaned_data['location']
            activity_name = activity_form.cleaned_data['activity_name']
            activity_introduction = activity_form.cleaned_data['activity_introduction']
            activity_requirements = activity_form.cleaned_data['activity_requirements']
            activity_start_time = activity_form.cleaned_data['activity_start_time']
            activity_end_time = activity_form.cleaned_data['activity_end_time']
            num = activity_form.cleaned_data['num']
            print("[DEBUG][POST][activity_name]:{}".format(activity_name))

            new_activity = Activity.objects.create(
                av_id=new_id, t=activity_type, l=location, a=admin, g=group,
                av_title=activity_name, av_state=activity_state,
                av_content=activity_introduction, av_request=activity_requirements,
                av_starttime=activity_start_time, av_endtime=activity_end_time,
                av_number=num
            )
            new_activity.save()
            messages.success(request, '发布活动成功！')
            # return show_activity(request)
            return redirect('/myapp/showActivity/')
        else:
            return render(request, 'activity/postActivity.html', locals())

    return render(request, 'activity/postActivity.html', locals())
