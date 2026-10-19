from django.urls import path
from .views import (RegisterView,Profil_viws,
                    Profil_update,Profil_detail,
                    ProfileSearchView,Avatar_cr,
                    Avatar_delet,ChatListCreateView,
                    ChatDetailDeleteView,MessageDeleteView,
                    MessageListCreateView,Group_cr,
                    GroupNumberListCreateView,
                    GroupNumberRoleUpdateView,
                    GroupNumberLeaveView,
                    GroupMessageListCreateView,
                    GroupMessageDeleteView,
                    ChanalListCreateView,ChanalDetailView,
                    PostListCreateView,
                    Group_delet,Group_update,Group_detail
                    )


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("profilecreat",Profil_viws.as_view()),
    path("profilupdate/<int:pk>/",Profil_update.as_view()),
    path("prfildetail",Profil_detail.as_view()),
    path('profiles/', ProfileSearchView.as_view()),
    path("avatar_cr",Avatar_cr.as_view()),
    path("avatar_delet",Avatar_delet.as_view()),
    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', ChatDetailDeleteView.as_view(), name='chat-detail'),
    path('chats/<int:chat_id>/messages/',MessageListCreateView.as_view(),name='message-list-create'),
    path('messages/<int:pk>/',MessageDeleteView.as_view(),name='message-delete'),
    path('group_cr',Group_cr.as_view()),
    path('groups/<int:group_id>/members/',GroupNumberListCreateView.as_view(),name='group-members'),
    path('groups/<int:group_id>/members/me/',GroupNumberLeaveView.as_view(),name='group-leave'),
    path('groups/<int:group_id>/members/<int:member_id>/',GroupNumberRoleUpdateView.as_view(),name='group-member-role'),
    path('groups/<int:group_id>/messages/',GroupMessageListCreateView.as_view(),name='group-message-list-create'),
    path('group-messages/<int:pk>/',GroupMessageDeleteView.as_view(),name='group-message-delete'),
    path('channels/', ChanalListCreateView.as_view()),
    path('channels/<int:pk>/', ChanalDetailView.as_view()),
    path('channels/<int:channel_id>/posts/',PostListCreateView.as_view(),name='post-list-create'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    
]


