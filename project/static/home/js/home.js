//  实现滑动轮播图
$(document).ready(function(){
    setTimeout(function(){
        swiper1();
        swiper2();
    }, 100);
});

function swiper1() {
    var mySwiper1 = new Swiper('#topSwiper', {
        direction: 'horizontal',
//        循环
        loop: true,
//        滑入速度
        speed: 500,
//        停留时间
        autoplay: 2000,
//        下面的控制小圆点
        pagination: '.swiper-pagination',
        control: true,
    });
};

function swiper2() {
    var mySwiper2 = new Swiper('#swiperMenu', {
        //一列显示三张图
        slidesPerView: 3,
        //可以点击
        paginationClickable: true,
        spaceBetween: 2,
        loop: false,
    });
};
