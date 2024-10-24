from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect, reverse, HttpResponse

# from django.core.mail import send_mail
# from .models import CaptchaModel
from django.http.response import JsonResponse
import string
import random
# Create your views here.
User = get_user_model()

def index_view(request):
    return render(request,'index.html')

def login_view(request):
    return render(request,'login.html')

# def send_email_captcha(request):
#     # ?email=xxx
#     email = request.GET.get('email')
#     if not email:
#         return JsonResponse({"code": 400, "message": '必须传递邮箱！'})
#     # 生成验证码（取随机的4位阿拉伯数字）
#     # ['0', '2', '9', '8']
#     captcha = "".join(random.sample(string.digits, 4))
#     # 存储到数据库中
#     CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
#     send_mail("共享系统的注册验证码", message=f"您的注册验证码是：{captcha}", recipient_list=[email],from_email=None)
#     return JsonResponse({"code": 200, "message": "邮箱验证码发送成功！"})

@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登录
                login(request, user)
                return redirect('/')
            else:
                form.add_error('email', '邮箱或密码错误！')
                return render(request, 'login.html', context={"form": form})
        else:
            # 如果表单无效，重新渲染页面并显示表单错误
            return render(request, 'login.html', context={"form": form})

@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('team_project:login'))
        else:
            print(form.errors)
            # 重新跳转到注册页面
            return redirect(reverse('team_project:register'))

def map_view(request):
    return render(request,template_name='map_merge_base.html')

