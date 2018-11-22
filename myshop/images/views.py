from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from images.models import Image
from images.forms import ImageModelForm


def list_image(request):
    template_name = 'images/list_image.html'

    results = Image.objects.all()

    return render(request, template_name, {'results': results})


def create_image(request):
    template_name = 'images/create_image.html'
    success_url = reverse_lazy('imagesapp:list_image')
    form = ImageModelForm(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid:
            form.save()
            return redirect(success_url)
        else:
            pass
    return render(request, template_name, {'form': form})


def update_image(request, **kwargs):
    template_name = 'images/update_image.html'
    success_url = reverse_lazy('imagesapp:list_image')
    pk = kwargs.get('pk')
    obj = Image.objects.get(pk=pk)
    form = ImageModelForm(instance=obj)

    if request.method == 'POST':
        form = ImageModelForm(
            request.POST,
            request.FILES,
            instance=obj
        )
        if form.is_valid:
            form.save()
            return redirect(success_url)
        else:
            pass
    return render(request, template_name, {'form': form, 'object': obj})


def detail_image(request, **kwargs):
    template_name = 'images/detail_image.html'
    pk = kwargs.get('pk')
    obj = Image.objects.get(pk=pk)

    return render(request, template_name, {'object': obj})


def delete_image(request, **kwargs):
    template_name = 'images/delete_image.html'
    success_url = reverse_lazy('imagesapp:list_image')
    pk = kwargs.get('pk')
    obj = Image.objects.get(pk=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect(success_url)
    return render(request, template_name, {'object': obj})
