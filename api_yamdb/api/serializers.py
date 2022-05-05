from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate(self, data):
        '''Валидируем, что пользователь не будет использовать
           никнейм, конфликтующий с эндпоинтом.
        '''
        if data.get('username') != 'me':
            return data
        raise serializers.ValidationError(
            'Невозможное имя пользователя'
        )


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        '''Валидируем, что пользователь не будет использовать
           никнейм, конфликтующий с эндпоинтом.
        '''
        if data.get('username') != 'me':
            return data
        raise serializers.ValidationError(
            'Невозможное имя пользователя'
        )


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    confirmation_code = serializers.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    class Meta:
        model = Genre
        fields = ('name', 'slug',)

class CategoryTitle(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreTitle(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryTitle(slug_field='slug', queryset=Category.objects.all(), required=False)
    genre = GenreTitle(slug_field='slug', queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title_id', 'author']
            )
        ]

        def validate_score(self, value):
            if value < 1 or value > 10:
                raise serializers.ValidationError('Недопустимое значение!')
            return value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review_id',)
