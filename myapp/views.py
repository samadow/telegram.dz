from django.shortcuts import render
from rest_framework import generics, permissions, status,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
# from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,ProfileSerializer,AvatarSerialezer,ChatSerializer,MessageSerializer,GroupSerializer
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListAPIView,DestroyAPIView
from .models import * 
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
class Profil_viws(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
   
class Profil_detail(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer 
    
class Profil_update(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    

class ProfileSearchView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'last_name', 'username']

class Avatar_cr(CreateAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerialezer
    
class Avatar_delet(DestroyAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerialezer
    
    

class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Chat.objects.filter(
            Q(user_1=user) | Q(user_2=user)
        ).order_by('-id')

    def perform_create(self, serializer):
        user = self.request.user
        other_user = serializer.validated_data['user_2']

        if user.id == other_user.id:
            raise ValidationError(
                {'user_2': 'Бо худат чат сохта намешавад.'}
            )

        chat_exists = Chat.objects.filter(
            Q(user_1=user, user_2=other_user) |
            Q(user_1=other_user, user_2=user)
        ).exists()

        if chat_exists:
            raise ValidationError(
                {'detail': 'Ин чат аллакай вуҷуд дорад.'}
            )

        serializer.save(user_1=user)


class ChatDetailDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Chat.objects.filter(
            Q(user_1=user) | Q(user_2=user)
        )
        
        

class MessagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MessagePagination

    def get_chat(self):
        return get_object_or_404(
            Chat.objects.filter(
                Q(user_1=self.request.user) |
                Q(user_2=self.request.user)
            ),
            id=self.kwargs['chat_id']
        )

    def get_queryset(self):
        chat = self.get_chat()

        return Message.objects.filter(
            chat_id=chat
        ).order_by('cr_at', 'id')

    def perform_create(self, serializer):
        chat = self.get_chat()

        serializer.save(
            sender=self.request.user,
            chat_id=chat
        )


class MessageDeleteView(generics.DestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            sender=self.request.user
        )
        
        
class Group_cr(CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class Group_detail(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class Group_delet(DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class Group_update(UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    