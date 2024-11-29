from django.urls import path
from friends.views import AddFriendsView, FriendListView


urlpatterns = [
    path('addFriends', AddFriendsView.as_view(), name='addFriends'),
    path('friendsList', FriendListView.as_view(), name='friendsList')    
]