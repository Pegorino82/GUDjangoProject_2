import datetime
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView

from authapp.models import AuthApp
from customers.models import Customer
from authapp.forms import CustomerAuthModelForm, CustomerLoginForm
from customers.views import CustomerCreateView


def log_auth_action(user, action='logup'):
    '''
    делаем отметку в бд о регистрации/входе/выходе пользователя
    :param user: user instance
    :param action: logup/login/logout
    :return:
    '''
    if user and user.is_active:
        auth_act = AuthApp.objects.create(user=user)
        if action == 'logup':
            auth_act.logup = datetime.datetime.now()
        elif action == 'login':
            auth_act.login = datetime.datetime.now()
        elif action == 'logout':
            auth_act.logout = datetime.datetime.now()
        auth_act.save()


class LogInView(LoginView):
    template_name = 'authapp/login.html'

    def get_success_url(self):
        return reverse_lazy('articlesapp:list')


class LogOutView(LogoutView):
    next_page = reverse_lazy('articlesapp:list')


# регистрация
class SignInView(CustomerCreateView):
    form_class = CustomerAuthModelForm
    template_name = 'authapp/logup.html'
    success_url = 'authapp/activation_key_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Sign In'})
        return context

    def form_valid(self, form):
        self.object = form.save()
        try:
            email = self.object.email
            send_mail(
                'Django',
                f'{self.object}, for finish registration go: '
                f'{settings.DOMAIN_NAME}/auth/verify/?email={email}&activation_key={self.object.activation_key}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            self.extra_context = {'email': email}
            return render(self.request, self.success_url, self.extra_context)
        except Exception as err:
            print('*' * 20)
            print('Sign in exception: ', err)
            print('*' * 20)
            return render(self.request, self.template_name)


###############ниже все то же, но на функциях + верификация по e-mail########

def login_view(request):
    success_url = reverse_lazy('articlesapp:list')
    login_form = CustomerLoginForm(request.POST)
    next = request.GET.get('next') if 'next' in request.GET.keys() else ''  # TODO
    context = {
        'next': next,
        'title': 'Login',
        'form': login_form
    }  # TODO
    if request.method == 'POST':
        usr_name = request.POST.get('username')
        psw = request.POST.get('password')
        user = authenticate(username=usr_name, password=psw)
        if user and user.is_active:
            log_auth_action(user, action='login')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST.keys():  # TODO
                return redirect(request.POST['next'])  # TODO
            else:  # TODO
                return redirect(success_url)  # TODO
        else:
            context.update(
                {
                    'user_name': usr_name,
                    'warn': 'incorrect username or password'
                }
            )
    return render(request, 'authapp/login.html', context)


def signin_view(request):
    '''
    регистрация пользователя с отправкой кода активации
    :param request:
    :return:
    '''
    success_url = 'authapp/activation_key_sent.html'
    template_name = 'authapp/logup.html'
    form = CustomerAuthModelForm(request.POST, request.FILES)
    context = {'title': 'Sign In'}
    if request.method == 'POST':
        if form.is_valid:
            try:
                user = form.save()
                email = user.email
                send_mail(
                    'Django',
                    f'{user}, for finish registration go: '
                    f'{settings.DOMAIN_NAME}/auth/verify/?email={email}&activation_key={user.activation_key}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                )
                context.update({'email': email})
                return render(request, success_url, context)
            except Exception as err:
                print('*' * 20)
                print('Sign in exception: ', err)
                print('*' * 20)
                return render(request, template_name, context)

    return render(request, template_name, {'form': form})


def logout_view(request):
    success_url = reverse_lazy('articlesapp:list')
    user = request.user
    log_auth_action(user, action='logout')
    logout(request)
    return redirect(success_url)


def verify(request):
    success_url = reverse_lazy('articlesapp:list')
    email = request.GET.get('email')
    activation_key = request.GET.get('activation_key')

    # залогиненного пользователя выводим из системы
    if request.user.is_authenticated:
        log_auth_action(request.user, action='logout')
        logout(request)

    try:
        user = Customer.objects.get(email=email, is_active=False)
        if user.activation_key == activation_key:
            user.is_active = True
            user.save()
            log_auth_action(user, 'logup')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            log_auth_action(user, action='login')
            return redirect(success_url)
        else:
            print('*' * 100)
            print(f'{user} activation error')
            print('*' * 100)
            return redirect(success_url)
    except Exception as err:
        print('*' * 100)
        print('verify view->>', err)
        print('*' * 100)
        return redirect(success_url)
