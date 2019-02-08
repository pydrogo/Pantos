from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate


class Login(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'login/login.html')

    def post(self, request, *args, **kwargs):
        try:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if (user is not None):
                if (user.is_active):
                    login(request, user)
                    return redirect('home')
                else:
                    msg = 'حساب شما غیر فعال است.'
                    return render(request, 'login/login.html',{'msg':msg} )
            else:
                msg = 'نام کاربری و یا رمز  ورود درست نمی باشد'
                return render(request, 'login/login.html', {'msg':msg})
        except:
            msg = 'خطایی رخ داده است لطفا مجددا تلاش کنید.'
            return render(request, 'login/login.html', {'msg': msg})

