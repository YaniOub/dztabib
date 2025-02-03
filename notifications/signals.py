from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
from .models import Notification
from MedApp.models import Appointment

@receiver(post_save, sender=Appointment)
def create_appointment_notification(sender, instance, created, **kwargs):
    # channel_layer = get_channel_layer()
    if created:
        # Appointment created
        message = f"Your appointment with Dr. {instance.doctor.user.username} has been created."
        Notification.objects.create(user=instance.patient.user, message=message)
        # async_to_sync(channel_layer.group_send)(
        #     f'notifications_{instance.patient.user.id}',
        #     {
        #         'type': 'send_notification',
        #         'message': message
        #     }
        # )
        message = f"An appointment with patient {instance.patient.user.username} has been created."
        Notification.objects.create(user=instance.doctor.user, message=message)
        # async_to_sync(channel_layer.group_send)(
        #     f'notifications_{instance.doctor.user.id}',
        #     {
        #         'type': 'send_notification',
        #         'message': message
        #     }
        # )
    else:
        # Appointment updated
        message = f"Your appointment with Dr. {instance.doctor.user.username} has been updated."
        Notification.objects.create(user=instance.patient.user, message=message)
        # async_to_sync(channel_layer.group_send)(
        #     f'notifications_{instance.patient.user.id}',
        #     {
        #         'type': 'send_notification',
        #         'message': message
        #     }
        # )
        message = f"An appointment with patient {instance.patient.user.username} has been updated."
        Notification.objects.create(user=instance.doctor.user, message=message)
        # async_to_sync(channel_layer.group_send)(
        #     f'notifications_{instance.doctor.user.id}',
        #     {
        #         'type': 'send_notification',
        #         'message': message
        #     }
        # )

@receiver(post_delete, sender=Appointment)
def delete_appointment_notification(sender, instance, **kwargs):
    # channel_layer = get_channel_layer()
    message = f"Your appointment with Dr. {instance.doctor.user.username} has been canceled."
    Notification.objects.create(user=instance.patient.user, message=message)
    # async_to_sync(channel_layer.group_send)(
    #     f'notifications_{instance.patient.user.id}',
    #     {
    #         'type': 'send_notification',
    #         'message': message
    #     }
    # )
    message = f"An appointment with patient {instance.patient.user.username} has been canceled."
    Notification.objects.create(user=instance.doctor.user, message=message)
    # async_to_sync(channel_layer.group_send)(
    #     f'notifications_{instance.doctor.user.id}',
    #     {
    #         'type': 'send_notification',
    #         'message': message
    #     }
    # )