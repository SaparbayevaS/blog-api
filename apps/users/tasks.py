from celery import shared_task

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retriess=3
)
def send_welcome_email(user_id):
    print(f"Send welcome email to user {user_id}")