from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import OfferResponse


@receiver(post_save, sender=OfferResponse)
def send_email_to_post_author(sender, instance, created, **kwargs):
    if created:
        # Получаем автора поста
        post_author = instance.post.author

        # Формируем сообщение
        subject = 'Получен новый отклик на ваш пост'
        message = f'Здравствуйте, {post_author.username}!\n\n' \
                  f'На ваш пост "{instance.post.title}" был оставлен новый отклик.\n\n' \
                  f'Содержание отклика:\n{instance.content}\n\n' \
                  f'Посмотреть отклик можно по следующему адресу: {settings.SITE_URL}/offer_response/{instance.id}/'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [post_author.email]

        # Отправляем письмо
        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=OfferResponse)
def send_email_to_post_author(sender, instance, created, **kwargs):
    if instance.is_accepted:
        # Проверяем, что у пользователя есть электронная почта
        if instance.client.email:
            send_mail(
                'Ваш отклик принят',
                f'Здравствуйте, {instance.client.username}!\n\nВаш отклик на пост "{instance.post.title}" был принят.',
                settings.DEFAULT_FROM_EMAIL,
                [instance.client.email],
                fail_silently=False,
            )
            