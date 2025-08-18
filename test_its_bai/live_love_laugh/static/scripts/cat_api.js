/**
 * Добавление картинки с котом на детальную страницу
*/ 
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector(".title-of-page");
    const fallbackUrl = '{% static "images/fallback-cat.jpg" %}';

    const img = document.createElement("img");
    img.src = fallbackUrl;
    img.classList.add('cat');
    img.alt = "Cat image";
    container.appendChild(img);

    async function loadCatImage() {
        try {
            const response = await fetch("https://api.thecatapi.com/v1/images/search", {
                mode: 'cors',
                cache: 'no-cache'
            });
            
            if (!response.ok) return;
            
            const data = await response.json();
            if (data && data[0]?.url) {
                const newImg = new Image();
                newImg.src = data[0].url;
                newImg.onload = function() {
                    img.src = this.src;
                };
            }
        } catch (error) {
            console.error('Cat API error:', error);
        }
    }

    loadCatImage();
});