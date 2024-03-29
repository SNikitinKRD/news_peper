from datetime import datetime, timedelta
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone

from .models import Post, PostCategory
from django.core.cache import cache
from .tasks import send_new_categories


@receiver(post_save, sender=Post)
def post_clear_cache(sender, instance, **kwargs):
    cache.delete(f'post-{instance.pk}')


@receiver(pre_save, sender=Post)
def check_count_users_posts(sender, instance, **kwargs):
    date_min = datetime.now(tz=timezone.utc) - timedelta(days=1)
    count = Post.objects.filter(author=instance.author, date_create__gte=date_min).count()
    print(count)
    if count>3:
        raise Exception('Нельзя публиковать больше трех постов в сутки')



@receiver(m2m_changed, sender=PostCategory)
def send_categories(sender, instance, action, **kwargs):
    if action != 'post_add':
        return
    send_new_categories.apply_async([instance.pk], countdown=5)

