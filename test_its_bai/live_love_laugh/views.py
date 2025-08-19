from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuoteForm
from .models import Quote, Like

"""
Главная страница со случайной цитатой

Создает сессию, если отсутствует
Получает случайную цитату через get_random() (Vose's Alias Method)
Увеличивает счетчик просмотров на 1
Проверяет, лайкнул ли пользователь (по session_key)
Передает в шаблон данные о цитате
"""
from django.db.models import Count
def index(request):
    if not request.session.session_key:
        request.session.create()
    quote = Quote.objects.get_random()
    quoteObj = Quote.objects.get(id=quote['id'])
    likes = quoteObj.total_likes
    if quote:

        Quote.increment_views_by_id(quote['id'])

        context = {
                'quote': quote,
                'show_details_link': True,
                'user_has_liked': quoteObj.user_has_liked(request.session.session_key),
                'likes': likes
            }
        return render(request, "index.html", context)

"""
Страница добавления цитаты

Проверяет валидность заполнения формы: если ок, сохраняем
""" 
def add(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            form = QuoteForm()
    else:
        form = QuoteForm()
           
    return render(request, 'add_quote.html', {'form': form})

"""
Список цитат с фильтрацией и сортировкой

По умолчанию сортировка по дате создания
Передает данные цитат и методы фильтрации
"""
def list(request):
    source_filter = request.GET.get('source')
    top_likes = request.GET.get('top_likes')
    top_views = request.GET.get('top_views')

    quotes = Quote.objects.all()
    
    if top_likes:
        
        if source_filter:
            quotes = quotes.filter(source__iexact=source_filter)
            
        quotes_with_ratings = [(q, q.total_likes) for q in quotes]
        quotes_with_ratings.sort(key=lambda x: x[1], reverse=True)
        quotes = [q[0] for q in quotes_with_ratings[:10]]
        show_top = True
        show_top_views = False
        
    elif top_views:
        quotes = Quote.objects.all()
        
        if source_filter:
            quotes = quotes.filter(source__iexact=source_filter)
            
        quotes = quotes.order_by('-views')[:10]
        show_top = False
        show_top_views = True
    else:
        quotes = Quote.objects.all()
        
        if source_filter:
            quotes = quotes.filter(source__iexact=source_filter)
            
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

"""
Детальная страница цитаты

Увеличивает счетчик просмотров на 1
Проверяет, лайкнул ли пользователь (по session_key)
Передает в шаблон данные о цитате
"""
def quote_details(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    Quote.increment_views_by_id(quote_id)
    context = {
        'quote': quote,
        'is_liked': False,
        'user_has_liked': quote.user_has_liked(request.session.session_key)
    }
    return render(request, 'quote_details.html', context)

"""
Страница с инструкцией
"""
def how_to(request):
    return render(request, 'how_to.html')

"""
Обработка постановки лайка

Создает/удаляет запись Like для quote_id + session_key
Корректирует счетчик лайков цитаты
Возвращает JSON
"""
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
        
    
    quote.save()
    return JsonResponse({
        'liked': created,  
        'total_likes': quote.total_likes
    })
    