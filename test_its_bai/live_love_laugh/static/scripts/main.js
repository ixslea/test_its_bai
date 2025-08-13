$(document).ready(function() {
    $('.like-button').click(function() {
        const button = $(this);
        const quoteId = button.data('quote-id');
        
        $.ajax({
            url: `/${quoteId}/like/`, 
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                button.toggleClass('liked', response.liked);
                const icon = button.find('.heart-icon');
                icon.removeClass('ri-heart-3-line ri-heart-3-fill')
                     .addClass(response.liked ? 'ri-heart-3-fill' : 'ri-heart-3-line');
                
            },
            error: function(xhr) {
                console.error('Error:', xhr.responseText);
            }
        });
    });
});

