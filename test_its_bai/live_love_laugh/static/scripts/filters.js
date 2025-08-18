document.addEventListener('DOMContentLoaded', function() {
    const filterButton = document.querySelector('.filter-tab-button');
    const closeButton = document.querySelector('.close-filter');
    const resetButton = document.querySelector('.reset-filters');
    const filterPanel = document.getElementById('filterPanel');
    const filterForm = document.getElementById('filterForm');
    const filterOptions = document.querySelectorAll('.filter-option');
    const sourceSelect = document.querySelector('.source-select');
    
    /**
     * Показ/скрытие панели фильтров
    */ 
    function toggleFilterPanel(e) {
        e.preventDefault();
        filterPanel.classList.toggle('active');
    }
    
    /**
     * Выбор опции фильтра
    */ 
    function selectOption(e) {
        e.preventDefault();
        const element = e.currentTarget;
        const group = element.parentElement;
        
        group.querySelectorAll('.filter-option').forEach(opt => {
            opt.classList.remove('active');
        });
        
        element.classList.add('active');
        
        if (element.textContent.includes('лайкам')) {
            document.getElementById('top_likes').value = '1';
            document.getElementById('top_views').value = '';
        } else if (element.textContent.includes('просмотрам')) {
            document.getElementById('top_views').value = '1';
            document.getElementById('top_likes').value = '';
        } else {
            document.getElementById('top_likes').value = '';
            document.getElementById('top_views').value = '';
        }
    }
    
    /**
     * Сброс фильтра
    */ 
    function resetFilters(e) {
        e.preventDefault();

        sourceSelect.value = '';
        
        document.querySelectorAll('.filter-group .filter-option').forEach((opt, index) => {
            opt.classList.remove('active');
            if (index === 0) opt.classList.add('active');
        });
        
        document.getElementById('top_likes').value = '';
        document.getElementById('top_views').value = '';
        
        filterForm.submit();
    }
    

    if (filterButton) filterButton.addEventListener('click', toggleFilterPanel);
    if (closeButton) closeButton.addEventListener('click', toggleFilterPanel);
    if (resetButton) resetButton.addEventListener('click', resetFilters);
    
    filterOptions.forEach(option => {
        option.addEventListener('click', selectOption);
    });
    
    document.querySelectorAll('.filter-option.active').forEach(opt => {
        if (opt.textContent.includes('лайкам')) {
            document.getElementById('top_likes').value = '1';
        } else if (opt.textContent.includes('просмотрам')) {
            document.getElementById('top_views').value = '1';
        }
    });
});