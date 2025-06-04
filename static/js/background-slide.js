const images = [
  '/static/images/bg1.jpg',
  '/static/images/bg2.jpg',
  '/static/images/bg3.jpg',
  '/static/images/bg4.jpg',
  '/static/images/bg5.jpg',
  '/static/images/bg6.jpg'  
];


let currentIndex = 0;
const bg1 = document.getElementById('bg1');
const bg2 = document.getElementById('bg2');

let showingBg1 = true;

// تنظیم اولین تصویر
bg1.style.backgroundImage = `url(${images[0]})`;
bg1.classList.add('active');

setInterval(() => {
  currentIndex = (currentIndex + 1) % images.length;

  if (showingBg1) {
    bg2.style.backgroundImage = `url(${images[currentIndex]})`;
    bg2.classList.add('active');
    bg1.classList.remove('active');
  } else {
    bg1.style.backgroundImage = `url(${images[currentIndex]})`;
    bg1.classList.add('active');
    bg2.classList.remove('active');
  }

  showingBg1 = !showingBg1;
}, 5000);
