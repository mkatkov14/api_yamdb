from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import User, Category, Genre, Title, Comment, Review


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
   # category = CategorySerializer(slug_field='slug', queryset=Category.objects.all(), required=False)
   # genre = GenreSerializer(slug_field='slug', queryset=Genre.objects.all(), many=True)

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
