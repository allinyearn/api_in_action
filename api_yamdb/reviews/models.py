from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Review(models.Model):
    """ Модель отзыва """
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    
    def __str__(self):
        """ Строковое представление объекта в поле text """
        return self.text


class Comment(models.Model):
    """ Модель коммента """
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        """ Строковое представление объекта в поле text """
        return self.text

