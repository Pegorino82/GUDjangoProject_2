from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404

from django.urls import reverse_lazy

from main.models import Author
from main.forms import MainAuthorForm, MainAuthorModelForm


def create_author(request):
    template_name = 'main/create_author.html'
    success_url = reverse_lazy('authorsapp:list')
    form = MainAuthorForm(request.POST)
    upl_img = request.FILES.get('photo')

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            lastname = form.cleaned_data.get('lastname')
            photo = upl_img
            Author.objects.create(
                name=name,
                lastname=lastname,
                photo=photo
            )
            return redirect(success_url)
    return render(request, template_name, {'form': form})


def update_author(request, **kwargs):
    template_name = 'main/update_author.html'
    success_url = reverse_lazy('authorsapp:list')
    pk = kwargs.get('pk')
    # obj = Author.objects.get(pk=pk)
    obj = get_object_or_404(Author, pk=pk)
    # TODO как заполнить поля формы полями выбранного объекта?
    form = MainAuthorForm()
    form.name = obj.name
    form.lastname = obj.lastname
    form.photo = obj.photo

    if request.method == 'POST':
        form = MainAuthorForm(
            request.POST
        )
        if form.is_valid:
            form.save()
            return redirect(success_url)
    return render(request, template_name, {'form': form, 'obj': obj})

def create_author_model_form(request):
    template_name = 'main/create_author.html'
    success_url = reverse_lazy('authorsapp:list')
    form = MainAuthorModelForm(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid:
            form.save()
            return redirect(success_url)
    return render(request, template_name, {'form': form})


def update_author_model_form(request, **kwargs):
    template_name = 'main/update_author.html'
    success_url = reverse_lazy('authorsapp:list')
    pk = kwargs.get('pk')
    # obj = Author.objects.get(pk=pk)
    obj = get_object_or_404(Author, pk=pk)
    form = MainAuthorModelForm(instance=obj)

    if request.method == 'POST':
        form = MainAuthorModelForm(
            request.POST,
            request.FILES,
            instance=obj
        )
        if form.is_valid:
            form.save()
            return redirect(success_url)
    return render(request, template_name, {'form': form, 'object': obj})


def detail_author(request, **kwargs):
    template_name = 'main/detail_author.html'
    pk = kwargs.get('pk')
    # obj = Author.objects.get(pk=pk)
    obj = get_object_or_404(Author, pk=pk)
    return render(request, template_name, {'object': obj})


def delete_author(request, **kwargs):
    template_name = 'main/delete_author.html'
    success_url = reverse_lazy('authorsapp:list')
    pk = kwargs.get('pk')
    # obj = Author.objects.get(pk=pk)
    obj = get_object_or_404(Author, pk=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect(success_url)
    return render(request, template_name, {'object': obj})


def list_author(request):
    template_name = 'main/list_author.html'
    context = {
        # 'results': Author.objects.all()
        'results': get_list_or_404(Author)
    }
    return render(request, template_name, context)