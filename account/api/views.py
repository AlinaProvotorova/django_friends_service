from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, FriendshipSerializer, FriendshipStatusSerializer
from account.models import Friendship


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint для регистрации нового пользователя.
    """
    serializer_class = UserSerializer


class SendFriendRequestView(generics.CreateAPIView):
    """
    API endpoint для отправки заявки в друзья другому пользователю.
    """
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        friend_id = request.data.get('friend')
        if friend_id is None:
            return Response(
                {'error': 'Friend ID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            friend = User.objects.get(id=friend_id)
            if friend.friends.filter(
                    friend=request.user,
                    is_accepted=False
            ).exists():
                friend.friends.filter(
                    friend=request.user
                ).update(is_accepted=True)
                request.user.friends.create(friend=friend, is_accepted=True)
                serializer = self.get_serializer(
                    instance=request.user.friends.get(friend=friend)
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                friend_request, created = request.user.friends.get_or_create(
                    friend=friend
                )
                serializer = self.get_serializer(instance=friend_request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(
                {'error': 'Friend not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class AcceptFriendRequestView(generics.UpdateAPIView):
    """
    API endpoint для принятия заявки в друзья.
    """
    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        friend_id = kwargs['pk']
        friend = get_object_or_404(User, id=friend_id)
        friend_request = get_object_or_404(
            Friendship,
            user=friend,
            friend=request.user
        )
        friend_request.is_accepted = True
        friend_request.save()
        Friendship.objects.create(
            user=request.user,
            friend=friend_request.user,
            is_accepted=True
        )
        return Response(
            {'success': 'Friend request accepted.'},
            status=status.HTTP_200_OK
        )


class RejectFriendRequestView(generics.DestroyAPIView):
    """
    API endpoint для отклонения заявки в друзья.
    """
    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        friend_id = kwargs['pk']
        friend = get_object_or_404(User, id=friend_id)
        friendship = get_object_or_404(
            Friendship,
            user=friend,
            friend=request.user
        )
        friendship.delete()
        return Response(
            {'success': 'Friend request reject.'},
            status=status.HTTP_200_OK
        )


class OutgoingFriendRequestsView(generics.ListAPIView):
    """
    API endpoint для получения списка исходящих заявок в друзья пользователя.
    """
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.filter(is_accepted=False)


class IncomingFriendRequestsView(generics.ListAPIView):
    """
    API endpoint для получения списка входящих заявок в друзья пользователя.
    """
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        return self.request.user.friend_of.filter(is_accepted=False)


class FriendsListView(generics.ListAPIView):
    """
    API endpoint для получения списка друзей пользователя.
    """
    serializer_class = FriendshipSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.friends.filter(is_accepted=True)


class FriendshipStatusView(generics.RetrieveAPIView):
    """
    API endpoint для получения статуса дружбы с конкретным пользователем.
    """
    serializer_class = FriendshipStatusSerializer
    queryset = Friendship.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        friend_id = self.kwargs.get('pk')
        friend = get_object_or_404(User, id=friend_id)
        status = self.get_friendship_status(request.user, friend)
        data = {
            'friend': friend,
            'status': status
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def get_friendship_status(self, user, friend):
        if user.friends.filter(friend=friend, is_accepted=True).exists():
            return "Already friends"
        elif user.friends.filter(friend=friend, is_accepted=False).exists():
            return "There is an outgoing request"
        elif user.friend_of.filter(user=friend, is_accepted=False).exists():
            return "There is an incoming application"
        else:
            return "Not friends"


class RemoveFriendView(generics.DestroyAPIView):
    """
    API endpoint для удаления пользователя из друзей.
    """
    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        friend_id = kwargs['pk']
        friend = get_object_or_404(User, id=friend_id)
        request.user.friends.filter(friend=friend).delete()
        friend.friends.filter(friend=request.user).delete()
        return Response(
            {'success': 'Friend removed.'},
            status=status.HTTP_200_OK
        )
