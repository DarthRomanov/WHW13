from django.forms import ModelForm, CharField, TextInput
from .models import Author
from .models import Quote


class AuthorForm(ModelForm):

    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Author
        fields = ['name']

class QuoteForm(ModelForm):

    name = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=150, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['name', 'description']
        exclude = ['author']