from django.shortcuts import render
from rest_framework import generics, permissions, status,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
# from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,ProfileSerializer,AvatarSerialezer,ChatSerializer,MessageSerializer,GroupSerializer,GroupNumberRoleSerializer,GroupNumberSerializer,GroupMessageSerializer,ChanalSerializer
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListAPIView,DestroyAPIView
from .models import * 
from rest_framework.exceptions import ValidationError,PermissionDenied
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
    
class GroupNumberListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupNumberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_group(self):
        return get_object_or_404(Group, id=self.kwargs['group_id'])

    def get_queryset(self):
        group = self.get_group()

        is_member = Group_number.objects.filter(
            group=group,
            user=self.request.user
        ).exists()

        if group.owner_id != self.request.user.id and not is_member:
            raise PermissionDenied('Ту иштирокчии ин гурӯҳ нестӣ.')

        return Group_number.objects.filter(group=group).select_related('user')

    def perform_create(self, serializer):
        group = self.get_group()
        user = self.request.user

        is_admin = Group_number.objects.filter(
            group=group,
            user=user,
            role='admin'
        ).exists()

        if group.owner_id != user.id and not is_admin:
            raise PermissionDenied(
                'Танҳо соҳиби гурӯҳ ё администратор иштирокчӣ илова мекунад.'
            )

        new_user = serializer.validated_data['user']

        if Group_number.objects.filter(
            group=group,
            user=new_user
        ).exists():
            raise ValidationError('Ин корбар аллакай иштирокчии гурӯҳ аст.')

        serializer.save(group=group, role='member')


class GroupNumberRoleUpdateView(generics.UpdateAPIView):
    serializer_class = GroupNumberRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch', 'head', 'options']
    lookup_url_kwarg = 'member_id'

    def get_queryset(self):
        group = get_object_or_404(Group, id=self.kwargs['group_id'])

        if group.owner_id != self.request.user.id:
            raise PermissionDenied('Танҳо соҳиби гурӯҳ метавонад рольро иваз кунад.')

        return Group_number.objects.filter(group=group)

    def get_object(self):
        member = super().get_object()

        if member.user_id == member.group.owner_id:
            raise ValidationError('Роли соҳиби гурӯҳро тағйир додан мумкин нест.')

        return member


class GroupNumberLeaveView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)

        if group.owner_id == request.user.id:
            raise ValidationError(
                'Соҳиби гурӯҳ баромада наметавонад. Аввал соҳибиро супоред.'
            )

        member = get_object_or_404(
            Group_number,
            group=group,
            user=request.user
        )

        member.delete()

        return Response({'detail': 'Ту аз гурӯҳ баромадӣ.'})
    
    
class GroupMessagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class GroupMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = GroupMessagePagination

    def get_group(self):
        group = get_object_or_404(
            Group,
            id=self.kwargs['group_id']
        )

        user = self.request.user

        is_member = Group_number.objects.filter(
            group=group,
            user=user
        ).exists()

        if group.owner_id != user.id and not is_member:
            raise PermissionDenied(
                'Ту иштирокчии ин гурӯҳ нестӣ.'
            )

        return group

    def get_queryset(self):
        group = self.get_group()

        return Group_message.objects.filter(
            group=group
        ).select_related('user').order_by('cr_at', 'id')

    def perform_create(self, serializer):
        group = self.get_group()

        serializer.save(
            user=self.request.user,
            group=group
        )


class GroupMessageDeleteView(generics.DestroyAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Group_message.objects.filter(
            user=self.request.user
        )
    
    


class ChannelListCreateView(generics.ListCreateAPIView):
    serializer_class = ChanalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Chanal.objects.filter(
            Q(type='public')
            | Q(owner=user)
            | Q(type='private', flowing__user_id=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ChanalListCreateView(generics.ListCreateAPIView):
    queryset = Chanal.objects.all()
    serializer_class = ChanalSerializer


class ChanalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chanal.objects.all()
    serializer_class = ChanalSerializer
    
    
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Post, Chanal
from .serializers import PostSerializer


# GET ва POST — рӯйхати постҳо ва сохтани пост
class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(
            chanal_id_id=self.kwargs['channel_id']
        ).order_by('-cr_at')

    def perform_create(self, serializer):
        channel = Chanal.objects.get(
            id=self.kwargs['channel_id']
        )

        if channel.owner != self.request.user:
            raise PermissionDenied(
                'Танҳо соҳиби канал метавонад пост созад.'
            )

        serializer.save(chanal_id=channel)


# GET, PATCH ва DELETE — як пост
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        post = self.get_object()

        if post.chanal_id.owner != self.request.user:
            raise PermissionDenied(
                'Танҳо соҳиби канал метавонад постро тағйир диҳад.'
            )

        serializer.save()

    def perform_destroy(self, instance):
        if instance.chanal_id.owner != self.request.user:
            raise PermissionDenied(
                'Танҳо соҳиби канал метавонад постро нест кунад.'
            )

        instance.delete()
        
        
 
 
 
 
 
         
# kjvnrwngwiojgwsopjvsweogjpjrg
# kjvnrwngwiojgwsopjvsweogjpjrg
# kjvnrwngwiojgwsopjvsweogjpjrg