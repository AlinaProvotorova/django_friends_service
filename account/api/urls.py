from django.urls import path

from . import views

urlpatterns = [
    path(
        'api/register/',
        views.UserRegistrationView.as_view(),
        name='register_user'
    ),
    path(
        'api/friends/',
        views.FriendsListView.as_view(),
        name='friends_list'
    ),
    path(
        'api/friends/remove/<int:pk>/',
        views.RemoveFriendView.as_view(),
        name='remove_friend'
    ),
    path(
        'api/friends/status/<int:pk>/',
        views.FriendshipStatusView.as_view(),
        name='friendship_status'
    ),
    path(
        'api/friend-request/send/',
        views.SendFriendRequestView.as_view(),
        name='send_friend_request'
    ),
    path(
        'api/friend-request/accept/<int:pk>/',
        views.AcceptFriendRequestView.as_view(),
        name='accept_friend_request'
    ),
    path(
        'api/friend-request/reject/<int:pk>/',
        views.RejectFriendRequestView.as_view(),
        name='reject_friend_request'
    ),
    path(
        'api/friend-request/outgoing/',
        views.OutgoingFriendRequestsView.as_view(),
        name='outgoing_friend_requests'
    ),
    path(
        'api/friend-request/incoming/',
        views.IncomingFriendRequestsView.as_view(),
        name='incoming_friend_requests'
    ),
]
