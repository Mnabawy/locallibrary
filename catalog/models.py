from django.db import models
from django.urls import reverse
import uuid


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='enter a book genre (science fection) ')


    def __str__(self):
        return self.name

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='enter aprief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13')
    genre = models.ManyToManyField(Genre, help_text='select a genre for this book') 


    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text = 'Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL,null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )    


    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book available',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """string for represinting the model object"""
        return f'{self.id}({self.book.title})'


'''Author model'''
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField(null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']
    
    def get_absolute_url(self):
        return reverse("author_detail", args=[str(self.id)])


    def __str__(self):
        return f'{self.last_name},{self.first_name}'
    

class Language(models.Model):
    name = models.CharField(max_length=250)
    book = models.ForeignKey("Book", on_delete=models.SET_NULL , null=True)

    def __str__(self):
        return self.name
    