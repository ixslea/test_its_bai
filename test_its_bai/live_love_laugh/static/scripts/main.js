/**
 * Обработчик лайков 
 */

$(document).ready(function() {
    /**
     * Обработчик клика по кнопке лайка
     */
    $('.like-btn').click(function() {
        const button = $(this);
        const quoteId = button.data('quote-id');
        const icon = button.find('.heart-icon');
        const likeCount = document.querySelector('.like-count');
        
        $.ajax({
            url: `/like/${quoteId}/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            /**
             * Обработчик успешного ответа от сервера
             */
            success: function(data) {
                    button.toggleClass('liked', data.liked);
                    icon.removeClass('ri-heart-3-line ri-heart-3-fill')
                         .addClass(data.liked ? 'ri-heart-3-fill' : 'ri-heart-3-line');

                    likeCount.textContent = data.total_likes;

                    icon.css('transform', 'scale(1.2)');
                    setTimeout(() => icon.css('transform', 'scale(1)'), 300);
                
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});

/**
 * Функция для получения значения cookie по имени
 */
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

