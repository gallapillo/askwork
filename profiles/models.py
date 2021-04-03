from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q


class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)

        accepted = []
        for rel in qs:
            if rel.status == 'accepted':
                accepted.append(rel.receiver)
                accepted.append(rel.sender)
        print(accepted)
        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    first_name = models.CharField(max_length=200, blank=True, verbose_name="Имя")
    second_name = models.CharField(max_length=200, blank=True, verbose_name="Фамилия")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    bio = models.TextField(default="О себе. ", max_length=300, verbose_name="Биография")
    email = models.EmailField(max_length=200, blank=True, verbose_name="Почта")
    country = models.CharField(max_length=200, blank=True, verbose_name="Страна")
    avatar = models.ImageField(default="avatar.png", upload_to="avatars/", verbose_name="Аватар")
    friends = models.ManyToManyField(User, blank=True, related_name='friends', verbose_name="Друзья")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Слог")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    objects = ProfileManager()

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_post_no(self):
        return self.posts.all().count()

    def fet_all_authors_post(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_likes_recieved_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    __initial_first_name = None
    __initial_second_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_second_name = self.second_name

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.second_name != self.__initial_second_name or self.slug == '':
            if self.first_name and self.second_name:
                to_slug = slugify(str(self.first_name) + ' ' + str(self.second_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + ' ' + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    objects = RelationshipManager()

    class Meta:
        verbose_name = "Отношение"
        verbose_name_plural = "Отношения"

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
