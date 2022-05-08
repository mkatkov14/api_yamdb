from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, User, Title, Review


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
    rating =rating = serializers.IntegerField(source='reviews__score__avg', read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    #def get_rating(self, obj):
    #    title = get_object_or_404(Title, id=obj.id) 
    #    reviews = title.reviews.all()
    ##    rat = reviews.aggregate(Avg('score'))
     #   return int(rat)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True, default=serializers.CurrentUserDefault(),
    )
    #title = SlugRelatedField(
    #    slug_field='title_id', read_only=True
    #)

    class Meta:
        #fields = '__all__'
        model = Review
        #read_only_fields = ('title',)
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

        def validate(self, data):
            title_id = self.context['view'].kwargs.get('title_id')
            author = self.context.get('request').user
            title = get_object_or_404(Title, id=title_id)
            if title.reviews.filter(author=author).exists() and self.context.get('request').method != 'PATCH':
                raise serializers.ValidationError(
                    'Вы уже оставляли здесь отзыв. До новых встреч.'
                )
            return data

        #def validate(self, data):
        #    if Review.objects.filter(
        #        title=self.context['view'].kwargs['title_id'],
        #        author=self.context['request'].user
        #    ).exists() and self.context['request'].method == 'POST':
        #        raise serializers.ValidationError(
        #            'Нельзя оставить два отзыва на одно произведение')
        #    return data

        #def validate(self, data):
        #    request = self.context.get('request')
        #    queryset = self.context.get('view').get_queryset()
        #    if queryset.filter(author=request.user).exists():
         #       raise serializers.ValidationError(
        #            'Нельзя оставлять больше 1 отзыва на произведение'
        #        )
        #    return data

        #def validate_score(self, value):
        #    if value < 1 or value > 10:
        #        raise serializers.ValidationError('Недопустимое значение!')
        #    return value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
