/**
 * Добавление картинки с котом на детальную страницу
*/ 
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector(".title-of-page");
    const img = document.createElement("img");
    img.classList.add('cat');

    async function fetchCatImage() {
        try {
            const response = await fetch("https://api.thecatapi.com/v1/images/search", {
                mode: 'cors',
                cache: 'no-cache',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            if (data?.[0]?.url) {
                const tempImg = new Image();
                tempImg.src = data[0].url;
                
                tempImg.onload = () => {
                    img.src = data[0].url;
                    container.appendChild(img);
                };
                return;
            }
            throw new Error('No image data received');
        } catch (error) {
            console.error('Error loading cat image:', error);
            showFallback();
        }
    }
    
    fetchCatImage();
});
