from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from .forms import QuoteForm
from .models import Quote, Like

def index(request):
    quote = Quote.objects.get_random()
    context = {'quote': quote} if quote else {}
    return render(request, "index.html", context)
 
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

@require_POST
def like_quote(request, quote_id):
    if not request.session.session_key:
        request.session.create()
    
    quote = Quote.objects.get(id=quote_id)
    session_key = request.session.session_key
    
    like, created = Like.objects.get_or_create(
        quote=quote,
        session_key=session_key,
        defaults={'quote': quote, 'session_key': session_key}
    )
    
    if not created:
        like.delete()
        quote.likes -= 1
        liked = False
    else:
        quote.likes += 1
        liked = True
    
    quote.save()
    return JsonResponse({
        'liked': liked,  
        'total_likes': quote.likes
    })
    