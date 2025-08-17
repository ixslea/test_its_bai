$(document).ready(function() {
    $('.like-btn').click(function() {
        const button = $(this);
        const quoteId = button.data('quote-id');
        const icon = button.find('.heart-icon');
        const likeCount = button.find('.like-count');
        
        $.ajax({
            url: `/like/${quoteId}/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data) {
                    // Переключаем класс кнопки
                    button.toggleClass('liked', data.liked);
                    
                    // Обновляем иконку
                    icon.removeClass('ri-heart-3-line ri-heart-3-fill')
                         .addClass(data.liked ? 'ri-heart-3-fill' : 'ri-heart-3-line');
                    
                    // Обновляем счетчик
                    if (likeCount.length) {
                        likeCount.text(data.total_likes);
                    }
                    
                    // Анимация
                    icon.css('transform', 'scale(1.2)');
                    setTimeout(() => icon.css('transform', 'scale(1)'), 300);
                
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

