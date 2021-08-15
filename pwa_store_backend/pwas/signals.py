from django.db.models.signals import post_save
from pwa_store_backend.pwas.models import Pwa, PwaAnalytics

def pwa_post_save_handler(sender, **kwargs):
    ''' created an instance of PWA Analytics when a new PWA is created '''
    instance = kwargs.get('instance')
    created = kwargs.get('created', False)
    if created:
        PwaAnalytics.objects.create(pwa=instance)

