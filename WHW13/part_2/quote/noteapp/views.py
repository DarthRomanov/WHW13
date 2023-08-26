from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorForm, QuoteForm
from .models import Author
from .models import Quote


# Create your views here.
def main(request):
    return render(request, 'noteapp/index.html')

def tag(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='noteapp:main')
        else:
            return render(request, 'noteapp/author.html', {'form': form})

    return render(request, 'noteapp/author.html', {'form': AuthorForm()})


def quote(request):
    author = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_author = Author.objects.filter(name__in=request.POST.getlist('author'))
            for author in choice_author.iterator():
                new_quote.author.add(author)

            return redirect(to='noteapp:main')
        else:
            return render(request, 'noteapp/quote.html', {"author": author, 'form': form})

    return render(request, 'noteapp/quote.html', {"author": author, 'form': QuoteForm()})
...

def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'noteapp/detail.html', {"quote": quote})
