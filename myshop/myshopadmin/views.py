from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.apps import apps
from collections import OrderedDict

from products.models import Product


class ModelCreate(LoginRequiredMixin, CreateView):
    template_name = 'myshopadmin/create.html'
    success_url = 'customersapp:customer'

    # def get_context_data(self, **kwargs):
    #     '''not used here'''
    #     context = super(ModelCreateProduct, self).get_context_data(**kwargs)
    #     context['app'] = self._app
    #     context['model'] = self._model
    #     return context

    def get(self, request, *args, **kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        self.model = apps.get_model(app, model.title())
        self.fields = [field.name for field in self.model._meta.__dict__.get('local_fields') if field.editable]
        return super(ModelCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        self.model = apps.get_model(app, model.title())
        self.fields = [field.name for field in self.model._meta.__dict__.get('local_fields') if field.editable]
        self.success_url = reverse_lazy('myshopadminapp:list', kwargs=kwargs)
        return super(ModelCreate, self).post(request)


class ModelUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'myshopadmin/update.html'
    success_url = 'customersapp:customer'

    def get(self, request, *args, **kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        pk = kwargs.get('pk')
        self.model = apps.get_model(app, model.title())
        self.object = self.model.objects.get(pk=pk)
        self.fields = [field.name for field in self.model._meta.__dict__.get('local_fields') if field.editable]
        return super(ModelUpdate, self).get(request, **kwargs)

    def post(self, request, *args, **kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        pk = kwargs.get('pk')
        self.model = apps.get_model(app, model.title())
        self.object = self.model.objects.get(pk=pk)
        self.fields = [field.name for field in self.model._meta.__dict__.get('local_fields') if field.editable]
        self.success_url = reverse_lazy('myshopadminapp:detail', kwargs=kwargs)
        return super(ModelUpdate, self).post(request)


class ModelDelete(LoginRequiredMixin, DeleteView):
    template_name = 'myshopadmin/delete.html'
    success_url = 'customersapp:customer'

    def get(self, request, *args, **kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        pk = kwargs.get('pk')
        self.model = apps.get_model(app, model.title())
        self.object = self.model.objects.get(pk=pk)
        self.fields = [field.name for field in self.model._meta.__dict__.get('local_fields') if field.editable]
        return super(ModelDelete, self).get(request, **kwargs)

    def post(self, request, *args, **kwargs):
        app = kwargs.get('app')
        model = kwargs.get('model')
        self.model = apps.get_model(app, model.title())
        self.fields = [field.name for field in self.model._meta.__dict__.get('local_fields') if field.editable]
        self.success_url = reverse_lazy('myshopadminapp:list', kwargs={'app': app, 'model': model})
        return super(ModelDelete, self).post(request)


class ModelDetail(LoginRequiredMixin, DetailView):
    template_name = 'myshopadmin/detail.html'
    context_object_name = 'results'
    success_url = 'customersapp:customer'

    def get(self, request, *args, **kwargs):
        self._app = kwargs.get('app')
        self._model = kwargs.get('model')
        self._pk = kwargs.get('pk')
        self.model = apps.get_model(self._app, self._model.title())
        self.object = self.model.objects.get(pk=self._pk)
        self.fields = [field.name for field in self.model._meta.__dict__.get('local_fields') if field.editable]
        return super(ModelDetail, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModelDetail, self).get_context_data(**kwargs)
        context['app'] = self._app
        context['model'] = self._model
        context['pk'] = self._pk
        context['included_template'] = 'myshopadmin/components/{}.html'.format(self._model.lower())
        return context


class ModelList(LoginRequiredMixin, ListView):
    template_name = 'myshopadmin/list.html'
    context_object_name = 'results'
    success_url = 'customersapp:customer'

    def get(self, request, *args, **kwargs):
        self._app = kwargs.get('app')
        self._model = kwargs.get('model')
        self.model = apps.get_model(self._app, self._model.title())
        self.fields = [field.name for field in self.model._meta.__dict__.get('local_fields') if field.editable]
        return super(ModelList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModelList, self).get_context_data(**kwargs)
        context['app'] = self._app
        context['model'] = self._model
        context['included_template'] = 'myshopadmin/components/{}.html'.format(self._model.lower())
        # context['included_template'] = 'oooooooooooo'
        return context


@login_required(login_url='customersapp:customer')
def index(request):
    all_apps = apps.get_models()

    get_apps = {item._meta.__dict__.get('app_label') for item in all_apps}

    get_apps_dict = OrderedDict().fromkeys(sorted(get_apps))

    prep_dict = {key: [] for key in get_apps_dict}

    for item in all_apps:
        prep_dict[item._meta.__dict__.get('app_label')].append(item._meta.__dict__.get('model_name'))

    # context = {'results': prep_dict}
    context = {
        'results': OrderedDict(sorted({
                                          'products': ('Product', 'Category', 'ProductMarker'),
                                          'images': ('Image',),
                                          'customers': ('Customer',),
                                          'main': ('Author', 'MainPageContent')
                                      }.items()))
    }

    return render(request, 'myshopadmin/index.html', context)
