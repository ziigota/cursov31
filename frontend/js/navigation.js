/**
 * Навигация по странице
 * Плавная прокрутка и подсветка активного раздела
 */

$(document).ready(function() {
    // Плавная прокрутка при клике на ссылку
    $('.nav-link').on('click', function(e) {
        e.preventDefault();

        const targetId = $(this).attr('href');
        const targetElement = $(targetId);

        if (targetElement.length) {
            // Убираем active у всех ссылок
            $('.nav-link').removeClass('active');

            // Добавляем active к текущей
            $(this).addClass('active');

            // Плавная прокрутка
            $('html, body').animate({
                scrollTop: targetElement.offset().top - 80 // 80px отступ для навигации
            }, 600);
        }
    });

    // Подсветка активного раздела при прокрутке
    $(window).on('scroll', function() {
        let current = '';

        $('.section').each(function() {
            const sectionTop = $(this).offset().top;
            const sectionHeight = $(this).height();

            if ($(window).scrollTop() >= sectionTop - 100) {
                current = $(this).attr('id');
            }
        });

        $('.nav-link').removeClass('active');
        $(`.nav-link[href="#${current}"]`).addClass('active');
    });
});