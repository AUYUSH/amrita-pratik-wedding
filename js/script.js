// Interactive Script for Amrita & Pratik Wedding Invitation

document.addEventListener('DOMContentLoaded', () => {
  // 1. Audio Control & Autoplay
  const audio = document.getElementById('wedding-audio');
  const audioBtn = document.getElementById('audio-toggle-btn');
  const coverScreen = document.getElementById('cover-screen');
  const openInviteBtn = document.getElementById('open-invite-btn');

  let isPlaying = false;

  function playAudio() {
    if (!audio) return;
    audio.play().then(() => {
      isPlaying = true;
      if (audioBtn) {
        audioBtn.classList.add('playing');
        audioBtn.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
          </svg>`;
      }
    }).catch(err => {
      console.log("Autoplay waiting for user gesture:", err);
    });
  }

  function pauseAudio() {
    if (!audio) return;
    audio.pause();
    isPlaying = false;
    if (audioBtn) {
      audioBtn.classList.remove('playing');
      audioBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
          <line x1="23" y1="9" x2="17" y2="15"></line>
          <line x1="17" y1="9" x2="23" y2="15"></line>
        </svg>`;
    }
  }

  function toggleAudio() {
    if (isPlaying) {
      pauseAudio();
    } else {
      playAudio();
    }
  }

  // Attempt autoplay on page load
  playAudio();

  if (openInviteBtn) {
    openInviteBtn.addEventListener('click', () => {
      // Fade out cover screen
      if (coverScreen) {
        coverScreen.classList.add('hidden-cover');
      }
      // Play audio on open invite
      playAudio();
    });
  }

  // Fallback autoplay trigger on first user interaction anywhere
  const firstTouchHandler = () => {
    if (!isPlaying) {
      playAudio();
    }
    window.removeEventListener('click', firstTouchHandler);
    window.removeEventListener('touchstart', firstTouchHandler);
  };
  window.addEventListener('click', firstTouchHandler);
  window.addEventListener('touchstart', firstTouchHandler);

  if (audioBtn) {
    audioBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleAudio();
    });
  }

  // 2. Live Countdown Timer (Target: Nov 26, 2026)
  const weddingDate = new Date('2026-11-26T19:00:00+05:30').getTime();

  function updateCountdown() {
    const now = new Date().getTime();
    const distance = weddingDate - now;

    if (distance < 0) {
      document.getElementById('days').innerText = '00';
      document.getElementById('hours').innerText = '00';
      document.getElementById('minutes').innerText = '00';
      document.getElementById('seconds').innerText = '00';
      return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById('days').innerText = days < 10 ? '0' + days : days;
    document.getElementById('hours').innerText = hours < 10 ? '0' + hours : hours;
    document.getElementById('minutes').innerText = minutes < 10 ? '0' + minutes : minutes;
    document.getElementById('seconds').innerText = seconds < 10 ? '0' + seconds : seconds;
  }

  setInterval(updateCountdown, 1000);
  updateCountdown();

  // 3. Interactive Gold Foil Scratch Card
  const canvas = document.getElementById('scratch-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let isDrawing = false;

    function resizeCanvas() {
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
      drawFoil();
    }

    function drawFoil() {
      if (!ctx) return;
      // Draw Gold Foil Gradient
      const grad = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      grad.addColorStop(0, '#fdf0a6');
      grad.addColorStop(0.3, '#c8a45d');
      grad.addColorStop(0.7, '#8e6922');
      grad.addColorStop(1, '#e5be6b');
      
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw Gold Shimmer Pattern & Text
      ctx.fillStyle = '#120b08';
      ctx.font = 'bold 12px Cinzel, serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('✦ SCRATCH GOLDEN FOIL TO REVEAL DATE ✦', canvas.width / 2, canvas.height / 2);
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function scratch(e) {
      if (!isDrawing) return;
      const rect = canvas.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      const x = clientX - rect.left;
      const y = clientY - rect.top;

      ctx.globalCompositeOperation = 'destination-out';
      ctx.beginPath();
      ctx.arc(x, y, 22, 0, Math.PI * 2);
      ctx.fill();
    }

    canvas.addEventListener('mousedown', (e) => { isDrawing = true; scratch(e); });
    canvas.addEventListener('mousemove', scratch);
    window.addEventListener('mouseup', () => { isDrawing = false; });

    canvas.addEventListener('touchstart', (e) => { isDrawing = true; scratch(e); });
    canvas.addEventListener('touchmove', scratch);
    window.addEventListener('touchend', () => { isDrawing = false; });
  }

  // 4. Scroll Reveal Animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.reveal-on-scroll').forEach(el => observer.observe(el));

  // 5. Blessings Form Handler
  const rsvpForm = document.getElementById('blessing-form');
  const toast = document.getElementById('toast-notification');

  if (rsvpForm) {
    rsvpForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('guest-name').value;
      
      // Show Toast Notification
      if (toast) {
        toast.innerText = `Thank you ${name}! Your blessings have been received. ❤️`;
        toast.classList.add('show');
        setTimeout(() => {
          toast.classList.remove('show');
        }, 4000);
      }
      rsvpForm.reset();
    });
  }
});
