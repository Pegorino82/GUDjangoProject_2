# GUDjangoProject_2
Continue to learn Django.

В репозитории есть БД с тестовыми продуктами, категориями и изображениями
Если БД нет, то необходимо выполнить следующие шаги:

1. python manage.py migrate

2. python manage.py fillimages test_images --del - добавить в бд тестовые картинки (--del предварительно удалить все из бд)
3. python manage.py fill_db --random - добавить в бд тестовые продукты

4. python manage.py add_authors test_mainpagecontent
5. python manage.py add_content test_mainpagecontent

Регистрация в приложении возможна через социальные сети VK и Google+,
а так же с подтверждением по e-mail, для этого надо запустить отладочный smtp сервер Python:

python -m smtpd -n -c DebuggingServer 0.0.0.0:25


