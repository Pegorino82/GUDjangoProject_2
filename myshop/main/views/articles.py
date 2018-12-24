from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from main.models import MainPageContent
from main.forms import MainArticleModelForm


class CreateArticleView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'main/create_article.html'
    success_url = reverse_lazy('articlesapp:list')
    form_class = MainArticleModelForm

    login_url = reverse_lazy('authapp:login_view')

    # @TODO определиться, кто может создавать статью
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Create Article'})
        return context


class ListArticleView(ListView):
    model = MainPageContent
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'List Articles'})
        return context


class DetailArticleView(DetailView):
    model = MainPageContent
    template_name = 'main/detail_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Detail Article'})
        return context


class UpdateArticleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MainPageContent
    template_name = 'main/update_article.html'
    form_class = MainArticleModelForm
    success_url = reverse_lazy('articlesapp:list')

    login_url = reverse_lazy('authapp:login_view')

    # @TODO определиться, кто может создавать статью
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Update Article'})
        return context


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MainPageContent
    template_name = 'main/delete_article.html'
    success_url = reverse_lazy('artivlesapp:list')

    # @TODO определиться, кто может удалить статью
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Delete Article'})
        return context


################################################################
#######function base views######################################
def list_article(request):
    template_name = 'main/index.html'
    context = {
        # 'results': MainPageContent.objects.all().order_by('-pk')
        'results': get_list_or_404(MainPageContent)[::-1]
    }

    return render(request, template_name, context)


def create_article(request):
    template_name = 'main/create_article.html'
    success_url = reverse_lazy('articlesapp:list')
    form = MainArticleModelForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(success_url)

    return render(request, template_name, {'form': form})


def update_article(request, **kwargs):
    template_name = 'main/update_article.html'
    success_url = reverse_lazy('articlesapp:list')
    pk = kwargs.get('pk')
    obj = MainPageContent.objects.get(pk=pk)
    obj = get_object_or_404(MainPageContent, pk=pk)

    # TODO надо передать в форму время из модели
    form = MainArticleModelForm(instance=obj)

    if request.method == 'POST':
        form = MainArticleModelForm(
            request.POST,
            instance=obj
        )
        if form.is_valid:
            form.save()
            return redirect(success_url)

    return render(request, template_name, {'form': form})


def detail_article(request, **kwargs):
    template_name = 'main/detail_article.html'
    pk = kwargs.get('pk')
    # obj = MainPageContent.objects.get(pk=pk)
    obj = get_object_or_404(MainPageContent, pk=pk)

    return render(request, template_name, {'object': obj})


def delete_article(request, **kwargs):
    template_name = 'main/delete_article.html'
    success_url = reverse_lazy('articlesapp:list')
    pk = kwargs.get('pk')
    # obj = MainPageContent.objects.get(pk=pk)
    obj = get_object_or_404(MainPageContent, pk=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect(success_url)

    return render(request, template_name, {'object': obj})
