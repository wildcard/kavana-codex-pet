(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const pet = document.querySelector('.pet');
  const frames = [0, 1, 2, 3, 2, 1];
  let index = 0;
  window.setInterval(() => {
    const column = frames[index++ % frames.length];
    pet.style.backgroundPosition = `${column * -192}px ${3 * -208}px`;
  }, 150);
})();
