from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """App-level role; super admins assign Admin vs User here."""

    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super admin'
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'

    def __str__(self):
        return f'{self.user.get_username()} ({self.get_role_display()})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Keep Django staff/superuser flags aligned with role (avoid recursive User.save).
        u = self.user
        if self.role == self.Role.SUPER_ADMIN:
            u.is_superuser = True
            u.is_staff = True
        elif self.role == self.Role.ADMIN:
            u.is_superuser = False
            u.is_staff = True
        else:
            u.is_superuser = False
            u.is_staff = False
        User.objects.filter(pk=u.pk).update(
            is_staff=u.is_staff,
            is_superuser=u.is_superuser,
        )
