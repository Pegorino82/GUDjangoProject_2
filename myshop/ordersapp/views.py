from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.db import transaction

from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderForm, OrderItemForm

from basket.models import Basket


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['user']
    # fields = []
    template_name = 'ordersapp/create.html'
    success_url = reverse_lazy('ordersapp:list')
    login_url = reverse_lazy('authapp:login_view')

    formset_model = OrderItem
    formset_form = OrderItemForm

    # basket = []

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_formset_class(self):

        self.basket = Basket.objects.filter(user=self.request.user.id).select_related()
        self.basket_ = Basket(user=self.request.user)

        # создаем формсет класс с помощью фабрики
        formset_class = inlineformset_factory(
            parent_model=self.model,
            model=self.formset_model,
            form=self.formset_form,
            extra=len(self.basket) or 1
        )
        return formset_class

    def get_formset_kwargs(self):
        # передаем именованные значения в формсет, в т.ч. файлы
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if hasattr(self, 'object'):
            kwargs.update(
                **{'instance': self.object}
            )
        return kwargs

    def get_formset(self):
        # создаем формсет на основе формсет класса
        formset_class = self.get_formset_class()
        formset_kwargs = self.get_formset_kwargs()
        formset = formset_class(**formset_kwargs)
        return formset

    def get_context_data(self, **kwargs):
        # передаем в контекс форму и формсет
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        formset = self.get_formset()

        total_cost = self.basket_.get_total_cost or 0
        # создаем заказ на основании корзины (которая на сервере)
        if len(self.basket):
            for count, item in enumerate(self.basket):
                formset.forms[count].initial['product'] = item.product
                formset.forms[count].initial['quantity'] = item.quantity
                formset.forms[count].initial['price'] = item.get_product_cost
                # total_cost = item.get_total_cost

        context.update(
            {
                'form': self.get_form(),
                'formset': formset,
                'total_cost': total_cost
            }
        )
        return context

    def get_form(self, form_class=None):
        # первоначально инициализируем форму пользователем
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
            form = form_class(**self.get_form_kwargs())
            form.initial['user'] = self.request.user.id
            return form
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            formset = self.get_formset()
            if formset.is_valid():
                formset.save()
                for item in self.basket:
                    item.delete()
                return redirect(self.success_url)
            return render(self.request, self.template_name)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'ordersapp/list.html'

    def get_queryset(self):
        # показываем поьзователю только его заказы
        return Order.objects.filter(user=self.request.user, is_active=True).select_related()


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'ordersapp/detail.html'
    context_object_name = 'order'


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    # fields = ['user']
    fields = []

    formset_model = OrderItem
    formset_form = OrderItemForm

    template_name = 'ordersapp/update.html'

    # success_url = reverse_lazy('ordersapp:detail')

    def get_formset_class(self):
        # создаем формсет класс с помощью фабрики
        formset_class = inlineformset_factory(
            parent_model=self.model,
            model=self.formset_model,
            form=self.formset_form,
            extra=0
        )
        return formset_class

    def get_formset(self):
        # создаем формсет с иницализацией текущей моделью
        formset_class = self.get_formset_class()
        if self.request.method == 'POST':
            formset = formset_class(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            formset = formset_class(instance=self.object)
        return formset

    def get_context_data(self, **kwargs):
        # передаем в контекс форму и формсет
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        formset = self.get_formset()
        for form in formset.forms:
            if form.instance.pk:
                form.initial['price'] = form.instance.get_order_item_price

        context.update(
            {
                'form': form,
                'formset': formset
            }
        )
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            formset = self.get_formset()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                # return redirect(self.success_url)
                return redirect('ordersapp:detail', self.object.pk)
            else:
                print('*' * 20)
                print('formset is not valid')
                print('*' * 20)
            return render(self.request, self.template_name)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    context_object_name = 'order'
    template_name = 'ordersapp/delete.html'
    success_url = reverse_lazy('ordersapp:list')


# отображение корзины на базе хранилища (localStorage)
# логика отображения на js
def storage(request, *args, **kwargs):
    template_name = 'ordersapp/storage.html'
    context = {}
    return render(request, template_name, context)
