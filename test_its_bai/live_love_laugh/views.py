from django.shortcuts import render, redirect
from .forms import QuoteForm
from .models import Quote

def index(request):
    data = {"cite": "lol"}
    return render(request, "index.html", context=data)
 
def add(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quote') 
    else:
        form = QuoteForm()
    
    return render(request, 'add_quote.html', {'form': form})

def list(request):
    quotes = Quote.objects.all().order_by('-create_date') 
    return render(request, 'list.html', {'quotes': quotes})
