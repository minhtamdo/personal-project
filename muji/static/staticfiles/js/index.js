var prevScrollpos = window.scrollY;
window.onscroll = function() {
  var currentScrollPos = window.scrollY;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("header_menu").style.top = "0";
  } else {
    document.getElementById("header_menu").style.top = "-100px";
  }
  prevScrollpos = currentScrollPos;
}

var responsiveSlider = function() {

  var slider = document.getElementById("promo-slider");
  var sliderWidth = slider.offsetWidth;
  var slideList = document.getElementById("slideWrap");
  var count = 1;
  var items = slideList.querySelectorAll("li").length;
  var prev = document.getElementById("prev");
  var next = document.getElementById("next");
  
  window.addEventListener('resize', function() {
    sliderWidth = slider.offsetWidth;
  });
  
  var prevSlide = function() {
    if(count > 1) {
      count = count - 2;
      slideList.style.left = "-" + count * sliderWidth + "px";
      count++;
    }
    else if(count === 1) {
      count = items - 1;
      slideList.style.left = "-" + count * sliderWidth + "px";
      count++;
    }
  };
  
  var nextSlide = function() {
    if(count < items) {
      slideList.style.left = "-" + count * sliderWidth + "px";
      count++;
    }
    else if(count === items) {
      slideList.style.left = "0px";
      count = 1;
    }
  };
  
  next.addEventListener("click", function() {
    nextSlide();
  });
  
  prev.addEventListener("click", function() {
    prevSlide();
  });
  
  setInterval(function() {
    nextSlide()
  }, 8000);
  
  };
  
document.addEventListener('DOMContentLoaded', function() {
    responsiveSlider();
});

var categorySlider = function() {

  var slider = document.getElementById("category-slider");
  var sliderWidth = slider.offsetWidth;
  var slideList = document.getElementById("slide-wrap");
  var count = 1;
  var items = slideList.querySelectorAll("li").length;
  var slide = items/6;
  var prev = document.getElementById("prev-cat");
  var next = document.getElementById("next-cat");
  
  window.addEventListener('resize', function() {
    sliderWidth = slider.offsetWidth;
  });
  
  var prevSlide = function() {
    if(count > 1) {
      count = count - 2;
      slideList.style.left = "-" + count * sliderWidth + "px";
      count++;
    }
    else if(count === 1) {
      count = slide - 1;
      slideList.style.left = "-" + count * sliderWidth + "px";
      count++;
    }
  };
  
  var nextSlide = function() {
    if(count < slide) {
      slideList.style.left = "-" + count * sliderWidth + "px";
      count++;
    }
    else if(count === slide) {
      slideList.style.left = "0px";
      count = 1;
    }
  };
  
  next.addEventListener("click", function() {
    nextSlide();
  });
  
  prev.addEventListener("click", function() {
    prevSlide();
  });
  
};
  
document.addEventListener('DOMContentLoaded', function() {
    categorySlider();
});

var responsiveSlider1 = function() {

  var slider = document.getElementById("promo-slider1");
  var sliderWidth = slider.offsetWidth;
  var slideList = document.getElementById("slideWrap1");
  var count = 1;
  var items = slideList.querySelectorAll("li").length;
  var prev = document.getElementById("prev1");
  var next = document.getElementById("next1");
  
  window.addEventListener('resize', function() {
    sliderWidth = slider.offsetWidth;
  });
  
  var prevSlide = function() {
    if(count > 1) {
      count = count - 2;
      slideList.style.left = "-" + count * sliderWidth + "px";
      count++;
    }
    else if(count === 1) {
      count = items - 1;
      slideList.style.left = "-" + count * sliderWidth + "px";
      count++;
    }
  };
  
  var nextSlide = function() {
    if(count < items) {
      slideList.style.left = "-" + count * sliderWidth + "px";
      count++;
    }
    else if(count === items) {
      slideList.style.left = "0px";
      count = 1;
    }
  };
  
  next.addEventListener("click", function() {
    nextSlide();
  });
  
  prev.addEventListener("click", function() {
    prevSlide();
  });
  
  setInterval(function() {
    nextSlide()
  }, 8000);
  
  };
  
document.addEventListener('DOMContentLoaded', function() {
    responsiveSlider1();
});
