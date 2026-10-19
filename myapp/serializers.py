from rest_framework import serializers
from .models import Acounts,Profile,Post,Chanal,Group,Group_message,Group_number,Chat,Message,Flowing,Avatar
from rest_framework import serializers





class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acounts
        fields = ('phone_number', 'password')

    def create(self, validated_data):
        phone = validated_data['phone_number']

        user = Acounts.objects.create_user(
            username=phone,
            phone_number=phone,
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['user_id']

class AvatarSerialezer(serializers.ModelSerializer):
    class Meta:
        model =  Avatar
        fields = "__all__"
        
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'user_1', 'user_2', 'cr_at']
        read_only_fields = ['id', 'user_1', 'cr_at'] 
        

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'chat_id', 'content', 'cr_at']
        read_only_fields = ['id', 'sender', 'chat_id', 'cr_at']
        
class GroupSerializer(serializers.ModelSerializer):
    model = Group
    fields = "__all__"
    