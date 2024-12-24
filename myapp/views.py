from django.shortcuts import render
from .forms import UserRegistrationForm
from .models import User

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.hashers import make_password
# Create your views here.

def index(request):
    return render(request, 'index.html')


def login_view(request):
    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

            if check_password(password, user.password):
                # Lưu thông tin đăng nhập vào session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('index')  # Chuyển hướng đến trang chủ
            else:
                message = "Mật khẩu không chính xác!"
        except User.DoesNotExist:
            message = "Tên đăng nhập không tồn tại!"

    return render(request, 'login.html', {'message': message})

# def login_view(request):
#     return render(request, 'login.html')

from django.shortcuts import render
from .models import User

def signup_view(request):
    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            message = "Mật khẩu không khớp!"
        elif User.objects.filter(username=username).exists():
            message = "Tên đăng nhập đã tồn tại!"
        elif User.objects.filter(email=email).exists():
            message = "Email đã được sử dụng!"
        else:
            hashed_password = make_password(password)
            User.objects.create(username=username, email=email, password=hashed_password)
            message = "Đăng ký thành công!"
    return render(request, 'signup.html', {'message': message})

def logout_view(request):
    request.session.flush()  # Xóa toàn bộ thông tin session
    return redirect('index')  # Chuyển hướng về trang chủ

def account_view(request):
    if not request.session.get('user_id'):
        return redirect('login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Kiểm tra trùng lặp
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            message = "Tên đăng nhập đã tồn tại!"
        elif User.objects.filter(email=email).exclude(id=user_id).exists():
            message = "Email đã được sử dụng!"
        else:
            user.username = username
            user.email = email
            user.save()
            message = "Thông tin đã được cập nhật thành công!"

    return render(request, 'account.html', {'user': user, 'message': message})

