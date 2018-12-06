from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from django.db import transaction

from ordersapp.models import Order, OrderItem
from basket.models import Basket

from ordersapp.forms import OrderForm, OrderItemForm


class OrderCreateView(CreateView):
    model = Order
    fields = []

    template_name = 'ordersapp/create.html'
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(OrderCreateView, self).get_context_data()
        OrderFormSet = inlineformset_factory(
            Order,
            OrderItem,
            form=OrderItemForm,
            extra=1
        )

        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST)
        else:
            user_basket = Basket.objects.filter(user=user)
            if user_basket:
                OrderFormSet = inlineformset_factory(
                    Order,
                    OrderItem,
                    form=OrderItemForm,
                    extra=len(user_basket)
                )
                formset = OrderFormSet()

                for idx, form in enumerate(formset.forms):
                    form.initial['product'] = user_basket[idx].product
                    form.initial['quantity'] = user_basket[idx].quantity
                # user_basket.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        form = self.get_form()

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            formset = orderitems
            if formset.is_valid:
                formset.instance = self.object
                # orderitems.instance = self.object
                # orderitems.save()
                formset.save()

                return redirect(self.success_url)

        return super(OrderCreateView, self).form_valid(form)


class OrderListView(ListView):
    model = Order
    template_name = 'ordersapp/list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
