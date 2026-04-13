from celery import shared_task


@shared_task(bind=True, max_retries=3)
def track_click(self, short_code):
    from .models import ShortURL
    from django.db.models import F

    try:
        ShortURL.objects.filter(short_code=short_code).update(
            click_count=F('click_count') + 1
        )
    except Exception as e:
        raise self.retry(exc=e, countdown=5)