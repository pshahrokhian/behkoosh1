document.addEventListener("DOMContentLoaded", function () {
  // --- تایپ متن ---
  const typingText = "مجتمع صنعتی بهکوش";
  const target = document.getElementById("typing-text");
  let index = 0;

  function type() {
    if (index <= typingText.length) {
      target.textContent = typingText.substring(0, index);
      index++;
      setTimeout(type, 100);
    }
  }

  type();

  // --- اسلایدر تصاویر سمت راست ---
  const sliderImages = [
    "/static/images/bg1.jpg",
    "/static/images/bg2.jpg",
    "/static/images/bg3.jpg"
  ];
  const slider = document.getElementById("slider-image");
  let sliderIndex = 0;

  setInterval(() => {
    sliderIndex = (sliderIndex + 1) % sliderImages.length;
    // افکت محو شدن تصویر هنگام تعویض
    slider.style.opacity = 0;
    setTimeout(() => {
      slider.src = sliderImages[sliderIndex];
      slider.style.opacity = 1;
    }, 500);
  }, 10000); // هر 10 ثانیه تصویر تغییر می‌کند
});
