import random
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm
from .forms import RegisterForm
from .models import Volunteer
from myapp.models import Apply
from django.contrib import messages


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
            volunteergroup = register_form.cleaned_data['volunteergroup']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'account/register.html', locals())
            else:
                same_id = Volunteer.objects.filter(v_name=username)
                if same_id:  # 同一个同学只能注册一个账号
                    message = '你已注册过'
                    return render(request, 'account/register.html', locals())
                else:
                    new_id = str(random.randint(0, 999999999))
                    old_id_list = Volunteer.objects.values_list("v_id")
                    while new_id in old_id_list:
                        new_id = str(random.randint(0, 999999999))
                    new_user = Volunteer.objects.create(v_id=new_id, v_name=username, v_pwd=password1, i=institute,vg=volunteergroup)
                    new_user.save()

                    # 自动跳转到登录页面
                    login_form = LoginForm()
                    messages.success(request, '注册成功！')
                    return redirect('/account/login/')
                    # return render(request, 'account/login.html', locals())  # 自动跳转到登录页面
    else:
        return render(request, 'account/register.html', locals())

    return render(request, 'account/register.html', locals())


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
                user_cus = Volunteer.objects.get(v_name=username)
                if user_cus.v_pwd == password:
                    messages.success(request, '{}登录成功！'.format(user_cus.v_name))
                    user_cus.save()
                    request.session['is_login'] = True
                    request.session['user_id'] = user_cus.v_id
                    request.session['user_name'] = user_cus.v_name
                    request.session['is_volunteer'] = True
                    request.session['institute'] = str(user_cus.i)
                    request.session['volunteerGroup'] = str(user_cus.vg)
                    return redirect('/showActivity/')
                    # return render(request, 'account/index.html', locals())
                else:
                    message = "密码不正确"
            except:
                message = "用户不存在"
    return render(request, 'account/login.html', locals())


def show_info(request):
    return render(request, 'account/show_info.html')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return render(request, 'account/index.html', locals())
    request.session.flush()
    messages.success(request, '您已成功退出登录')
    return redirect('/')


def applyResult(request):
    volunteer = Volunteer.objects.filter(v_id=request.session['user_id']).first()
    template_name = 'account/applyList.html'
    context = {'application_list': Apply.objects.filter(v=volunteer)}
    return render(request, template_name, context)
