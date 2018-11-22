from django.db import models


class AuthApp(models.Model):
    user = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE
    )

    _logup = models.DateTimeField(
        # auto_now_add=True,
        null=True,
        blank=True
    )
    _login = models.DateTimeField(
        # auto_now=True,
        null=True,
        blank=True
    )
    _logout = models.DateTimeField(
        # auto_now=True,
        null=True,
        blank=True
    )

    @property
    def logup(self):
        return self._logup

    @logup.setter
    def logup(self, time=None):
        if time:
            self._logup = time

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, time=None):
        if time:
            self._login = time

    @property
    def logout(self):
        return self._logout

    @logout.setter
    def logout(self, time=None):
        if time:
            self._logout = time

    def __str__(self):
        action = None
        if self._logup:
            action = 'logup'
        elif self._login:
            action = 'login'
        elif self._logout:
            action = 'logout'
        return f'{self.user.username} / {action}'
