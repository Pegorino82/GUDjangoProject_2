from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def contacts(request):
    context = {}
    # print(request.POST)
    if request.method == "POST":
        usr_name = request.POST.get('username')
        email = request.POST.get('email')
        text = request.POST.get('text')
        send_mail(
            'Django',
            text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        # context.update({
        #     'usr_name': usr_name,
        #     'email': email,
        #     'text': text
        # })

    return render(request, 'contacts/contacts.html', context)
