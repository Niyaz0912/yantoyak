// static/js/map_detail.js

document.addEventListener('DOMContentLoaded', function() {
    
    // Ждем, пока загрузится API Яндекс.Карт
    ymaps.ready(function () {
        
        // Создаем карту в контейнере id="map"
        const map = new ymaps.Map('map', {
            center: [54.7388, 55.9721], // Координаты Уфы
            zoom: 7,
            controls: ['zoomControl', 'searchControl', 'typeSelector', 'fullscreenControl'],
        });

        console.log('Карта успешно создана!');
    });
});