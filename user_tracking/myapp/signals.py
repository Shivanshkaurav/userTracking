from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, pre_save, pre_delete
from django.forms.models import model_to_dict
from django.dispatch import receiver
from .models import TodoTracking
from .mixins import TrackableMixin


@receiver(user_logged_in)
def log_in_user(sender, request, user, **kwargs):
    TodoTracking.objects.create(
        user = user,
        action = 'Login',
        model_name = user.__class__.__name__,
        model_instance_id = user.id,
        details = f"User {user.username} logged in"
    )

@receiver(user_logged_out)
def log_out_user(sender, request, user, **kwargs):
    TodoTracking.objects.create(
        user = user,
        action = 'Logout',
        model_name = user.__class__.__name__,
        model_instance_id = user.id,
        details = f"User {user.username} logged out"
    )

@receiver(post_save)
def track_creation(sender, instance, created, **kwargs):
    if created and isinstance(instance, TrackableMixin):
        instance.track_changes('Created')
        
@receiver(pre_save)
def track_update(sender, instance, **kwargs):
    if instance.pk and isinstance(instance, TrackableMixin):
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            old_data = model_to_dict(old_instance)
            new_data = model_to_dict(instance)
            
            changes = {
                field: (old_data.get(field), new_data.get(field))
                for field in new_data
                if old_data.get(field) != new_data.get(field)
            }
            
            if changes:
                details = "; ".join(
                    [f"{field.capitalize()} changed from {old} to {new}" for field, (old, new) in changes.items()]
                )
                instance.track_changes('Updated', details=details)
        except sender.DoesNotExist:
            pass

# @receiver(pre_delete)
# def track_deletion(sender, instance, **kwargs):
#     if isinstance(instance, TrackableMixin):
#         details = f"Deleted {instance.__class__.__name__} items: {getattr(instance, 'title', 'N/A')}"
#         instance.track_changes('Deleted', details=details)
    
@receiver(pre_delete)
def track_deletion(sender, instance, **kwargs):
    if isinstance(instance, TrackableMixin):
        instance.track_changes('Deleted')
