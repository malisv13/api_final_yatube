from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Попытка подписаться самого на себя!'
            )
        return data

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]
