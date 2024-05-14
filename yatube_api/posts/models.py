from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class RelatedName():

    class Meta:
        default_related_name = '%(class)ss'


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        blank=True, null=True
    )

    class Meta(RelatedName.Meta):
        ordering = ('pub_date', 'author')

    def __str__(self):
        return f'{self.text[:8]} {self.pub_date} {self.author}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta(RelatedName.Meta):
        ordering = ('created', 'author')


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follows'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('following',)
