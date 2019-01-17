from django.shortcuts import render
from contacts.models import Feedback


# сохраняет в бд имя отправителя, почту и текст сообщения
def contacts(request):
    context = {}
    if request.method == "POST":
        user = request.user
        email = request.POST.get('email')
        text = request.POST.get('text')
        if user.is_authenticated:
            feedback = Feedback.objects.create(
                user=user,
                email=email,
                text=text
            )
            feedback.save()
        else:
            feedback = Feedback.objects.create(
                email=email,
                text=text
            )
            feedback.save()

    return render(request, 'contacts/contacts.html', context)
