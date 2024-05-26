from users.models import User
from products.models import Notification


def add_notification(user_id, notification_msg):
    if user_id == None:
        return None
    else:
        data = {}
        data["recipient"] = user_id
        data["content"] = notification_msg
        person = Notification.objects.create(
            recipient=user_id, content=notification_msg
        )
        return True
