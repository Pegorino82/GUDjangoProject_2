from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView

from main.models import MainPageContent
from main.forms import MainArticleModelForm


class ArticleView(ListView):
    model = MainPageContent
    template_name = 'main/index.html'


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
