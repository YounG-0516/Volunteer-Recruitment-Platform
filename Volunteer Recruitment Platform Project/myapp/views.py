import random
from django.shortcuts import render, get_object_or_404, redirect
from .forms import LoginForm
from .forms import RegisterForm
from activity.forms import ActivityForm
from .models import Administrator, Apply
from activity.models import Activity
from account.models import Volunteer
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

def apply(request):
    template_name = 'myapp/activity_list.html'
    # context = {'activity_list': Activity.objects.all()}
    context = {'activity_list': Activity.objects.filter(Q(av_endtime__gt=timezone.now()))}
    return render(request, template_name, context)



def show_activity(request):
    template_name = 'myapp/activity_list_admin.html'
    admin = Administrator.objects.filter(a_id=request.session['user_id']).first()
    context = {'activity_list_admin': Activity.objects.filter(a=admin)}  # 只有正在招募志愿者的活动才能被申请
    return render(request, template_name, context)


def submit_application(request, activity_id):
    activity = get_object_or_404(Activity, av_id=activity_id)
    user_id = request.session['user_id']

    user = Volunteer.objects.filter(v_id=user_id).first()
    new_id = str(random.randint(0, 999999999))
    old_id_list = Apply.objects.values_list("ap_id")
    while new_id in old_id_list:
        new_id = str(random.randint(0, 999999999))
    now_apply_list = Apply.objects.values_list("av")
    if activity.a not in now_apply_list:
        application = Apply.objects.create(ap_id=new_id, a=activity.a, v=user, av=activity, ap_time=timezone.now(),
                                           ap_state=2, ap_reason="无")
        application.save()
        messages.success(request, '申请成功，请耐心等待活动管理员审核')
        return redirect('/showActivity/')
    else:
        messages.success(request, '您已申请过该活动')
        return render(request, 'myapp/activity_list_admin.html', locals())

def register(request):
    register_form = RegisterForm()

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            institute = register_form.cleaned_data['institute']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'myapp/register.html', locals())
            else:
                same_id = Administrator.objects.filter(a_name=username)
                if same_id:  # 同一个同学只能注册一个账号
                    message = '你已注册过'
                    return render(request, 'myapp/register.html', locals())
                else:
                    new_id = str(random.randint(0, 999999999))
                    old_id_list = Administrator.objects.values_list("a_id")
                    while new_id in old_id_list:
                        new_id = str(random.randint(0, 999999999))
                    new_user = Administrator.objects.create(a_id=new_id, a_name=username, a_pwd=password1, i=institute)
                    new_user.save()

                    # 自动跳转到登录页面
                    login_form = LoginForm()
                    messages.success(request, '注册成功！')
                    return redirect('/myapp/login/')
                    # return render(request, 'account/login.html', locals())  # 自动跳转到登录页面
    else:
        return render(request, 'myapp/register.html', locals())

    return render(request, 'myapp/register.html', locals())


def login(request):
    login_form = LoginForm()

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            print("[DEBUG][POST][LOGIN][username]:{}".format(username))
            print("[DEBUG][POST][LOGIN][password]:{}".format(password))
            try:
                user_cus = Administrator.objects.get(a_name=username)
                if user_cus.a_pwd == password:
                    messages.success(request, '{}登录成功！'.format(user_cus.a_name))
                    user_cus.save()
                    request.session['is_login'] = True
                    request.session['user_id'] = user_cus.a_id
                    request.session['user_name'] = user_cus.a_name
                    request.session['is_volunteer'] = False
                    request.session['institute'] = str(user_cus.i)
                    return redirect('/myapp/showActivity/')
                    # return render(request, 'account/index.html', locals())
                else:
                    message = "密码不正确"
            except:
                message = "用户不存在"
    return render(request, 'myapp/login.html', locals())


def check(request):
    template_name = 'myapp/apply_list.html'
    admin = Administrator.objects.filter(a_id=request.session['user_id']).first()
    context = {'application_list': Apply.objects.filter(a=admin)}
    return render(request, template_name, context)


def approve(request, application_id):
    application = Apply.objects.filter(ap_id=application_id).first()
    application.ap_state = 1
    application.ap_approvaltime = timezone.now()
    application.save()
    return check(request)


def reject(request, application_id):
    application = Apply.objects.filter(ap_id=application_id).first()
    application.ap_state = 3
    application.ap_approvaltime = timezone.now()
    application.save()
    return check(request)

def editActivity(request):
    activity_form = ActivityForm()

    if request.method == "POST":
        activity_form = ActivityForm(request.POST)

        print(activity_form.is_valid())
        errors = activity_form.errors.as_data()
        for field, error_list in errors.items():
            for error in error_list:
                print(f"{field}: {error}")

        if activity_form.is_valid():  # 获取数据
            activity_type = activity_form.cleaned_data['activity_type']
            group = activity_form.cleaned_data['group']
            location = activity_form.cleaned_data['location']
            activity_name = activity_form.cleaned_data['activity_name']
            activity_introduction = activity_form.cleaned_data['activity_introduction']
            activity_requirements = activity_form.cleaned_data['activity_requirements']
            activity_start_time = activity_form.cleaned_data['activity_start_time']
            activity_end_time = activity_form.cleaned_data['activity_end_time']
            num = activity_form.cleaned_data['num']

            activity_record = Activity.objects.filter(av_title=activity_name).first()

            activity_record.t = activity_type
            activity_record.l = location
            activity_record.g = group
            activity_record.av_content = activity_introduction
            activity_record.av_request = activity_requirements
            activity_record.av_starttime = activity_start_time
            activity_record.av_endtime = activity_end_time
            activity_record.av_number = num
            activity_record.save()

            messages.success(request, '修改活动成功！')
            return redirect('/myapp/showActivity/')

        else:
            return render(request, 'myapp/editActivity.html', locals())

    return render(request, 'myapp/editActivity.html', locals())


def deleteActivity(request, activity_id):
    apply_records = Apply.objects.filter(av=activity_id)
    apply_records.delete()
    activity_record = Activity.objects.filter(av_id=activity_id)
    activity_record.delete()
    return show_activity(request)