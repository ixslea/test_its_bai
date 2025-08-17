from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import QuoteForm
from .models import Quote, Like
from django.shortcuts import get_object_or_404, render


def index(request):
    if not request.session.session_key:
        request.session.create()
    quote = Quote.objects.get_random()
    quoteObj = Quote.objects.get(id=quote['id'])
    if quote:

        Quote.increment_views_by_id(quote['id'])

        context = {
                'quote': quote,
                'show_details_link': True,
                'user_has_liked': quoteObj.user_has_liked(request.session.session_key)
            }
        return render(request, "index.html", context)
 
def add(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            form = QuoteForm()
    else:
        form = QuoteForm()
           
    return render(request, 'add_quote.html', {'form': form})

def list(request):
    if request.GET.get('top_likes') and request.GET.get('top_views'):
        params = request.GET.copy()
        params.pop('top_likes', None)
        params.pop('top_views', None)
        return redirect(f"{request.path}?{params.urlencode()}")

    source_filter = request.GET.get('source')
    top_likes = request.GET.get('top_likes')
    top_views = request.GET.get('top_views')
    
    quotes = Quote.objects.all()
    
    if source_filter:
        quotes = quotes.filter(source__iexact=source_filter)
    
    if top_likes:
        quotes = quotes.order_by('-likes')[:10] 
        show_top = True
        show_top_views = False
    elif top_views:
        quotes = quotes.order_by('-views')[:10] 
        show_top = False
        show_top_views = True
    else:
        quotes = quotes.order_by('-create_date') 
        show_top = False
        show_top_views = False
    
    sources = Quote.objects.values_list('source', flat=True).distinct()
    
    return render(request, 'list.html', {
        'quotes': quotes,
        'sources': sources,
        'current_source': source_filter,
        'show_top': show_top,
        'show_top_views': show_top_views,
        'quotes_count': Quote.objects.count() 
    })


def quote_details(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    Quote.increment_views_by_id(quote_id)
    context = {
        'quote': quote,
        'is_liked': False,
        'user_has_liked': quote.user_has_liked(request.session.session_key)
    }
    return render(request, 'quote_details.html', context)

def how_to(request):
    return render(request, 'how_to.html')

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
    