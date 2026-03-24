 

  //$(document).ready(function(){
//    $('.slider').bxSlider({ auto:true });
//});

$(document).ready(function(){
$('.slider').bxSlider({ auto:true, mode:'fade', controls:false, pager:true, touchEnabled:false, speed: 1000 });
$('.testimonial').bxSlider({ auto:true, mode:'horizontal', controls:true , pager: false, touchEnabled:true, speed: 500 });
$('.mainplace').bxSlider({ auto:true, mode:'horizontal', controls: true , responsive:true, pager: false, border:0,touchEnabled:true, speed: 500});

});



$(function() {
$(window).scroll(function() {
if($(this).scrollTop() != 0) {
$('#top').fadeIn();
} else {
$('#top').fadeOut();
}
});
$('#top').click(function() {
$('body,html').animate({scrollTop:0},500);
});
});


// topscroling
const backToTopButton = document.querySelector("#back-to-top-btn");

window.addEventListener("scroll", scrollFunction);

function scrollFunction() {
  if (window.pageYOffset > 300) { // Show backToTopButton
    if(!backToTopButton.classList.contains("btnEntrance")) {
      backToTopButton.classList.remove("btnExit");
      backToTopButton.classList.add("btnEntrance");
      backToTopButton.style.display = "block";
    }
  }
  else { // Hide backToTopButton
    if(backToTopButton.classList.contains("btnEntrance")) {
      backToTopButton.classList.remove("btnEntrance");
      backToTopButton.classList.add("btnExit");
      setTimeout(function() {
        backToTopButton.style.display = "none";
      }, 250);
    }
  }
}

backToTopButton.addEventListener("click", smoothScrollBackToTop);

// function backToTop() {
//   window.scrollTo(0, 0);
// }

function smoothScrollBackToTop() {
  const targetPosition = 0;
  const startPosition = window.pageYOffset;
  const distance = targetPosition - startPosition;
  const duration = 750;
  let start = null;
  
  window.requestAnimationFrame(step);

  function step(timestamp) {
    if (!start) start = timestamp;
    const progress = timestamp - start;
    window.scrollTo(0, easeInOutCubic(progress, startPosition, distance, duration));
    if (progress < duration) window.requestAnimationFrame(step);
  }
}

function easeInOutCubic(t, b, c, d) {
  t /= d/2;
  if (t < 1) return c/2*t*t*t + b;
  t -= 2;
  return c/2*(t*t*t + 2) + b;
};


// smoothScrollBackToTop


$(document).ready(function(){
 let scroll_link = $('.scroll');

  //smooth scrolling -----------------------
  scroll_link.click(function(e){
      e.preventDefault();
      let url = $('body').find($(this).attr('href')).offset().top;
      $('html, body').animate({
        scrollTop : url
      },700);
      $(this).parent().addClass('active');
      $(this).parent().siblings().removeClass('active');
      return false; 
   });
});

// popupmenu
// active -menu
