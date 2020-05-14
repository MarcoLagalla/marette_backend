from django.urls import path
from .views import AllNotifications, UnReadCount, UnReadList, MarkAsRead , MarkAsUnread

app_name = 'orders'

urlpatterns = [
    path('', AllNotifications.as_view(), name='all_notifications'),
    path('unread_list', UnReadList.as_view(), name='list_unread'),
    path('unread_count', UnReadCount.as_view(), name='count_unread'),
    path('notification/<int:id>/mark_as_read', MarkAsRead.as_view(), name='mark_as_read'),
    path('notification/<int:id>/mark_as_unread', MarkAsUnread.as_view(), name='mark_as_unread'),
]
