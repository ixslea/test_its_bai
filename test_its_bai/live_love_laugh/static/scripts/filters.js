/**
 * Показ/скрытие панели фильтров
*/ 
function toggleFilterPanel() {
    const panel = document.getElementById('filterPanel');
    panel.classList.toggle('active');
}

/**
 * Выбор опции фильтра
*/ 
function selectOption(element, name, value) {
    const group = element.parentElement;
    const options = group.querySelectorAll('.filter-option');
    options.forEach(opt => opt.classList.remove('active'));

    element.classList.add('active');

    if (name === 'top_likes') {
        document.getElementById('top_likes').value = value;
    }

    if (name === 'top_views') {
        document.getElementById('top_views').value = value;
    }
}

/**
 * Сброс фильтра
*/ 
function resetFilters() {
    document.querySelector('.source-select').value = '';

    const sortOptions = document.querySelectorAll('.filter-group .filter-option');
    sortOptions.forEach(opt => opt.classList.remove('active'));
    sortOptions[0].classList.add('active');
    document.getElementById('top_likes').value = '';
    document.getElementById('top_views').value = '';

    document.getElementById('filterForm').submit();
}

document.addEventListener('DOMContentLoaded', function() {
    const filterButton = document.querySelector('.filter-tab-button');
    if (filterButton) {
        filterButton.addEventListener('click', toggleFilterPanel);
    }

    const closeButton = document.querySelector('.close-filter');
    if (closeButton) {
        closeButton.addEventListener('click', toggleFilterPanel);
    }

    const resetButton = document.querySelector('.reset-filters');
    if (resetButton) {
        resetButton.addEventListener('click', resetFilters);
    }

});