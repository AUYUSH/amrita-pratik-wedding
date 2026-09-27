(() => {
  const media = {
    audio: { directory: './assets/media/audio', chunks: 12, type: 'audio/mpeg' },
    video: { directory: './assets/media/video', chunks: 59, type: 'video/mp4' },
  };

  const pathsFor = ({ directory, chunks }) =>
    Array.from({ length: chunks }, (_, index) =>
      `${directory}/${String(index).padStart(3, '0')}.bin`,
    );

  async function objectUrlFor(config) {
    const responses = await Promise.all(pathsFor(config).map(async (path) => {
      const response = await fetch(path, { cache: 'force-cache' });
      if (!response.ok) throw new Error(`Unable to load ${path}`);
      return response.arrayBuffer();
    }));
    return URL.createObjectURL(new Blob(responses, { type: config.type }));
  }

  document.addEventListener('DOMContentLoaded', () => {
    const audio = document.getElementById('wedding-audio');
    const video = document.querySelector('.hero-video');
    const openInvite = document.getElementById('open-invite-btn');
    const audioButton = document.getElementById('audio-toggle-btn');
    if (!audio || !video) return;

    // The cover portrait belongs only to the opening screen; show video after invite opens.
    audio.removeAttribute('src');
    video.removeAttribute('poster');
    video.querySelectorAll('source').forEach((source) => source.remove());
    video.load();

    const ready = Promise.all([objectUrlFor(media.audio), objectUrlFor(media.video)])
      .then(([audioUrl, videoUrl]) => {
        audio.src = audioUrl;
        video.src = videoUrl;
        audio.load();
        video.load();
        return { audio, video };
      })
      .catch((error) => {
        console.error('Wedding media could not be prepared:', error);
        throw error;
      });

    const begin = () => ready.then(({ audio: loadedAudio, video: loadedVideo }) => {
      loadedVideo.play().catch(() => {});
      loadedAudio.play().then(() => {
        audioButton?.classList.add('playing');
      }).catch(() => {});
    }).catch(() => {});

    // Capture ensures these run before the original invite/audio handlers.
    openInvite?.addEventListener('click', begin, true);
    audioButton?.addEventListener('click', begin, true);
  });
})();
