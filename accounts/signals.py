from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, **kwargs):
    """Ensure a profile exists; keep superuser and Super admin role in sync.

    createsuperuser can save the User twice (non-superuser first). If we only
    promoted role on profile_created, the second save would leave role=USER and
    staff/superuser flags cleared by UserProfile.save().
    """
    if kwargs.get('raw'):
        return
    role_default = (
        UserProfile.Role.SUPER_ADMIN
        if instance.is_superuser
        else UserProfile.Role.USER
    )
    profile, _ = UserProfile.objects.get_or_create(
        user=instance,
        defaults={'role': role_default},
    )
    if instance.is_superuser and profile.role != UserProfile.Role.SUPER_ADMIN:
        profile.role = UserProfile.Role.SUPER_ADMIN
        profile.save(update_fields=['role'])


def _recipient_email(user):
    if user is None:
        return None
    email = getattr(user, 'email', '') or ''
    return email.strip() or None


def _send_mail(subject, message, recipient):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception as exc:
        # With DEBUG=True you will see this in the runserver terminal if SMTP fails.
        if settings.DEBUG:
            print(f'[EMAIL ERROR] {exc}')


@receiver(user_logged_in)
def notify_login_email(sender, request, user, **kwargs):
    to = _recipient_email(user)
    if not to:
        if settings.DEBUG:
            print('[EMAIL] Skipped: user has no email address set.')
        return
    _send_mail(
        'Login successful',
        (
            f'Hello {user.get_username()},\n\n'
            'You have logged in successfully.\n\n'
            'If this was not you, secure your account immediately.\n'
        ),
        to,
    )


@receiver(user_logged_out)
def notify_logout_email(sender, request, user, **kwargs):
    to = _recipient_email(user)
    if not to:
        if settings.DEBUG:
            print('[EMAIL] Skipped: user has no email address set.')
        return
    _send_mail(
        'Logout successful',
        (
            f'Hello {user.get_username()},\n\n'
            'You have been logged out successfully.\n\n'
            'Thank you for using our site.\n'
        ),
        to,
    )
