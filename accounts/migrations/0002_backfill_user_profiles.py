from django.db import migrations


def backfill_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('accounts', 'UserProfile')
    for u in User.objects.all():
        if UserProfile.objects.filter(user_id=u.pk).exists():
            continue
        role = 'super_admin' if u.is_superuser else 'user'
        UserProfile.objects.create(user_id=u.pk, role=role)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(backfill_profiles, migrations.RunPython.noop),
    ]
