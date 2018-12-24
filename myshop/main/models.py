from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    photo = models.ImageField(
        upload_to='authors/',
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.lastname)

    def __repr__(self):
        return '{} {}'.format(self.name, self.lastname)


class MainPageContent(models.Model):
    chapter = models.CharField(max_length=150)
    content = models.TextField()
    author = models.ForeignKey(
        'main.Author',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} (author {})'.format(self.chapter[:10],
                                          self.content[:10],
                                          self.author)
