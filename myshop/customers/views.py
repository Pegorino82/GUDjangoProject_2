from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
# from django.contrib.auth import authenticate, login, logout, get_user
# from django.contrib.auth.views import LoginView
# from django.db.utils import IntegrityError
# from django.http import HttpResponse, Http404
from django.db import transaction

from customers.models import Customer
from customers.forms import CustomerCreateForm, CustomerUpdateForm, CustomerModelForm, CustomerProfileModelForm


# class CustomerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
class CustomerCreateView(CreateView):

    form_class = CustomerCreateForm
    template_name = 'customers/create.html'
    success_url = reverse_lazy('customersapp:list')

    # login_url = reverse_lazy('authapp:login_view')
    #
    # def test_func(self):
    #     return self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Create Customer'})
        return context


class CustomerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''Просмотр списка пользователей реализован
    для закрепления CRUD, для использования админом'''
    model = Customer
    template_name = 'customers/list.html'
    paginate_by = 3

    login_url = reverse_lazy('authapp:login_view')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'List Customer'})
        return context


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': self.request.user})
        return context


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'customers/update.html'
    form_class = CustomerUpdateForm
    success_url = reverse_lazy('customersapp:detail')

    login_url = reverse_lazy('authapp:login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Update Customer'})
        return context


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customers/delete.html'
    success_url = reverse_lazy('customersapp:list')

    login_url = reverse_lazy('authapp:login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Delete Customer'})
        return context


@user_passes_test(lambda user: user.is_superuser or user.is_staff, login_url='authapp:login_view')
@login_required(login_url='customersapp:customer')
def create_customer(request):
    template_name = 'customers/create_customer.html'
    success_url = reverse_lazy('customersapp:list_customer')
    # form = CustomerModelForm(request.POST, request.FILES)
    form = CustomerCreateForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            return redirect(success_url)
    return render(request, template_name, {'form': form})


# Редактирование профиля пользователя
@transaction.atomic
@login_required(login_url='authapp:login_view')
def edit_profile(request, **kwargs):
    template_name = 'customers/edit_profile.html'
    pk = kwargs.get('pk')
    success_url = reverse_lazy('customersapp:detail', kwargs={'pk': pk})

    if request.method == 'POST':
        edit_form = CustomerUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = CustomerProfileModelForm(request.POST, instance=request.user.customerprofile)
        if edit_form.is_valid and profile_form.is_valid:
            edit_form.save()
            profile_form.save()
            return redirect(success_url)
    else:
        edit_form = CustomerUpdateForm(instance=request.user)
        profile_form = CustomerProfileModelForm(instance=request.user.customerprofile)
    return render(request, template_name, {
        'form': edit_form,
        'profile_form': profile_form,
        'title': 'Edit Profile'
    })


# для редактирования пользователя со стороны админа
@user_passes_test(lambda user: user.is_superuser or user.is_staff, login_url='authapp:login_view')
@login_required(login_url='customersapp:customer')
def update_customer(request, **kwargs):
    template_name = 'customers/update_customer.html'
    success_url = reverse_lazy('customersapp:list_customer')
    pk = kwargs.get('pk')
    obj = Customer.objects.get(pk=pk)
    # TODO сделать автозаполнение DateInput данными из модели
    form = CustomerModelForm(instance=obj)
    if request.method == 'POST':
        form = CustomerModelForm(
            request.POST,
            request.FILES,
            instance=obj
        )
        if form.is_valid:
            form.save()
            return redirect(success_url)
    return render(request, template_name, {'form': form})


@user_passes_test(lambda user: user.is_superuser or user.is_staff, login_url='authapp:login_view')
@login_required(login_url='customersapp:customer')
def detail_customer(request, **kwargs):
    template_name = 'customers/detail_customer.html'
    pk = kwargs.get('pk')
    obj = Customer.objects.get(pk=pk)
    return render(request, template_name, {'object': obj})


@user_passes_test(lambda user: user.is_superuser or user.is_staff, login_url='authapp:login_view')
@login_required(login_url='customersapp:customer')
def list_customer(request):
    template_name = 'customers/list_customer.html'
    results = Customer.objects.all()
    return render(request, template_name, {'results': results})


@user_passes_test(lambda user: user.is_superuser or user.is_staff, login_url='authapp:login_view')
@login_required(login_url='customersapp:customer')
def delete_customer(request, **kwargs):
    template_name = 'customers/delete_customer.html'
    success_url = reverse_lazy('customersapp:list_customer')
    pk = kwargs.get('pk')
    obj = Customer.objects.get(pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect(success_url)
    return render(request, template_name, {'object': obj})


def login_view(request):
    notification = {}
    return render(request, 'customers/customer.html', notification)
