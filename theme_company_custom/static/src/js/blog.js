$(document).ready(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop()) {
            $('#gototop').fadeIn();
        } else {
            $('#gototop').fadeOut();
        }
    });
    $("#gototop").click(function () {
        $("html, body").animate({scrollTop: 0}, 1000);
    });
    $(".image-gallery").lightSlider({
        item: 5,
        loop: true,
        auto: true,
        slideMove: 1,
        easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
        speed: 600,
        responsive: [
            {
                breakpoint: 800,
                settings: {
                    item: 3,
                    slideMove: 1,
                    slideMargin: 6,
                    loop: true,
                    auto: true,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    item: 2,
                    slideMove: 1,
                    loop: true,
                    auto: true,
                }
            }
        ]
    });
    $(".videos-slide").lightSlider({
        item: 1,
        loop: true,
        auto: true,
        slideMove: 1,
        speed: 600,
        slideMargin: 3,
        onSliderLoad: function() {
            $( window ).resize();
        }, onAfterSlide: function() {
            $( window ).resize();
        },
        responsive: [
            {
                breakpoint: 800,
                settings: {
                    item: 1,
                    slideMove: 1,
                    slideMargin: 6,
                    loop: true,
                    auto: true,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    item: 1,
                    slideMove: 1,
                    loop: true,
                    auto: true,
                }
            }
        ]
    });
});
setInterval(function () {
    // var d = new Date();
    var d = new Date().toLocaleString("vi-VN", {
        "timezone": "Asia/Ho_Chi_Minh",
        "dateStyle": "full",
        "timeStyle": "medium"
    });
    $("#date-time > p").html(d);
}, 1000);