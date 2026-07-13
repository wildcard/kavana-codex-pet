(() => {
  'use strict';

  document.documentElement.classList.add('js');

  const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  let reducedMotion = reducedMotionQuery.matches;

  const rowFrames = (row, durations) => durations.map((duration, column) => ({ row, column, duration }));
  const states = {
    idle: rowFrames(0, [280, 110, 110, 140, 140, 320]),
    runRight: rowFrames(1, [120, 120, 120, 120, 120, 120, 120, 220]),
    runLeft: rowFrames(2, [120, 120, 120, 120, 120, 120, 120, 220]),
    wave: rowFrames(3, [140, 140, 140, 280]),
    jump: rowFrames(4, [140, 140, 140, 140, 280]),
    failed: rowFrames(5, [140, 140, 140, 140, 140, 140, 140, 240]),
    waiting: rowFrames(6, [150, 150, 150, 150, 150, 260]),
    work: rowFrames(7, [120, 120, 120, 120, 120, 220]),
    review: rowFrames(8, [150, 150, 150, 150, 150, 280]),
    look: [
      ...rowFrames(9, [190, 150, 150, 150, 190, 150, 150, 150]),
      ...rowFrames(10, [190, 150, 150, 150, 190, 150, 150, 240]),
    ],
    sleep: [
      { row: 5, column: 2, duration: 320 },
      { row: 5, column: 3, duration: 420 },
      { row: 5, column: 4, duration: 1200 },
      { row: 5, column: 5, duration: 520 },
      { row: 5, column: 4, duration: 1200 },
    ],
  };

  class SpriteAnimator {
    constructor(element, scale = 1) {
      this.element = element;
      this.scale = scale;
      this.stateName = 'idle';
      this.frameIndex = 0;
      this.timer = 0;
      this.loop = true;
    }

    paint(frame) {
      this.element.style.backgroundPosition = `${-frame.column * 192 * this.scale}px ${-frame.row * 208 * this.scale}px`;
    }

    show(stateName, frameIndex = 0) {
      window.clearTimeout(this.timer);
      this.stateName = states[stateName] ? stateName : 'idle';
      this.frameIndex = frameIndex;
      this.paint(states[this.stateName][this.frameIndex] || states[this.stateName][0]);
    }

    play(stateName, { loop = true, stillFrame = 0 } = {}) {
      window.clearTimeout(this.timer);
      this.stateName = states[stateName] ? stateName : 'idle';
      this.frameIndex = reducedMotion ? stillFrame : 0;
      this.loop = loop;
      this.paint(states[this.stateName][this.frameIndex] || states[this.stateName][0]);
      if (!reducedMotion) this.schedule();
    }

    schedule() {
      const frames = states[this.stateName];
      const frame = frames[this.frameIndex];
      this.timer = window.setTimeout(() => {
        if (!this.loop && this.frameIndex >= frames.length - 1) return;
        this.frameIndex = (this.frameIndex + 1) % frames.length;
        this.paint(frames[this.frameIndex]);
        this.schedule();
      }, frame.duration);
    }

    refreshForMotionPreference() {
      this.play(this.stateName, { loop: this.loop, stillFrame: this.stateName === 'sleep' ? 4 : 0 });
    }
  }

  const wait = (duration, token, currentToken) => new Promise((resolve) => {
    window.setTimeout(() => resolve(token === currentToken()), reducedMotion ? Math.min(duration, 80) : duration);
  });

  function initHeroPlayground() {
    const playground = document.querySelector('[data-playground]');
    const stage = document.querySelector('[data-pet-stage]');
    const pet = document.querySelector('[data-hero-pet]');
    const sprite = pet?.querySelector('[data-sprite]');
    const speech = document.querySelector('[data-speech]');
    const actionLabel = document.getElementById('action-label');
    const tourButton = document.querySelector('[data-action="tour"]');
    const tourLabel = tourButton?.querySelector('[data-tour-label]');
    const actionButtons = [...document.querySelectorAll('.pet-actions [data-action]')];
    if (!playground || !stage || !pet || !sprite || !speech || !actionLabel || !tourButton || !tourLabel) return;

    const animator = new SpriteAnimator(sprite);
    let actionToken = 0;
    let tourActive = !reducedMotion;
    let currentAction = 'wave';

    const actionCopy = {
      zoomies: ['Purposeful zoomies', 'Fast is a valid direction.'],
      roam: ['Following the trail', 'I’ll inspect everything.'],
      wave: ['A little hello', 'Hi! I’m Kavana.'],
      jump: ['Tiny victory jump', 'That deserves a hop.'],
      look: ['Sixteen curious looks', 'Something interesting over there…'],
      work: ['Getting to work', 'Intention, then action.'],
      review: ['Reviewing the evidence', 'Let me check that twice.'],
      sleep: ['Taking a field nap', 'Zzz… wake me for the next task.'],
      idle: ['Keeping good company', 'I’m right here.'],
    };

    const updateTourButton = () => {
      tourButton.setAttribute('aria-pressed', String(tourActive));
      tourLabel.textContent = reducedMotion ? 'Motion reduced' : tourActive ? 'Pause tour' : 'Play full tour';
      tourButton.querySelector('.tour-icon').textContent = tourActive ? 'Ⅱ' : '▶';
      tourButton.disabled = reducedMotion;
    };

    const announce = (action, customSpeech) => {
      const [label, words] = actionCopy[action] || actionCopy.idle;
      actionLabel.textContent = label;
      speech.classList.add('is-changing');
      window.setTimeout(() => {
        speech.textContent = customSpeech || words;
        speech.classList.remove('is-changing');
      }, reducedMotion ? 0 : 130);
      actionButtons.forEach((button) => button.classList.toggle('is-active', button.dataset.action === action));
    };

    const moveTo = (xRatio, yRatio, travel = 800) => {
      const petWidth = window.innerWidth <= 620 ? 142 : 192;
      const petHeight = window.innerWidth <= 620 ? 154 : 208;
      const maxX = Math.max(0, stage.clientWidth - petWidth);
      const maxY = Math.max(0, stage.clientHeight - petHeight);
      pet.style.setProperty('--pet-x', `${Math.round(maxX * xRatio)}px`);
      pet.style.setProperty('--pet-y', `${Math.round(maxY * yRatio)}px`);
      pet.style.setProperty('--travel', `${reducedMotion ? 0 : travel}ms`);
    };

    const valid = (token) => token === actionToken;
    const pause = (duration, token) => wait(duration, token, () => actionToken);

    const setState = (name, options) => animator.play(name, options);

    async function runAction(action, token) {
      currentAction = action;
      announce(action);

      if (reducedMotion) {
        const stillStates = {
          zoomies: 'runRight', roam: 'look', wave: 'wave', jump: 'jump',
          look: 'look', work: 'work', review: 'review', sleep: 'sleep',
        };
        const state = stillStates[action] || 'idle';
        setState(state, { loop: false, stillFrame: state === 'sleep' ? 4 : 0 });
        return;
      }

      if (action === 'wave') {
        moveTo(.16, .62, 700);
        setState('wave');
        await pause(1900, token);
      } else if (action === 'jump') {
        moveTo(.48, .35, 650);
        setState('jump');
        await pause(1800, token);
      } else if (action === 'look') {
        moveTo(.72, .42, 900);
        setState('look');
        await pause(3200, token);
      } else if (action === 'work') {
        moveTo(.5, .62, 850);
        setState('work');
        await pause(2400, token);
        if (!valid(token)) return;
        currentAction = 'review';
        announce('review', 'Task done. Evidence first.');
        setState('review');
        await pause(2100, token);
      } else if (action === 'review') {
        moveTo(.52, .58, 700);
        setState('review');
        await pause(2300, token);
      } else if (action === 'sleep') {
        moveTo(.12, .66, 800);
        setState('sleep', { loop: false, stillFrame: 4 });
        await pause(3500, token);
      } else if (action === 'zoomies') {
        setState('runRight');
        moveTo(.82, .66, 900);
        if (!await pause(950, token)) return;
        setState('runLeft');
        moveTo(.06, .65, 900);
        if (!await pause(950, token)) return;
        setState('runRight');
        moveTo(.7, .18, 780);
        if (!await pause(820, token)) return;
        setState('jump');
        announce('zoomies', 'One celebratory hop!');
        if (!await pause(900, token)) return;
        setState('runLeft');
        moveTo(.2, .58, 750);
        await pause(820, token);
      } else if (action === 'roam') {
        setState('runRight');
        moveTo(.54, .15, 1500);
        if (!await pause(1550, token)) return;
        setState('look');
        announce('roam', 'Lookout checked.');
        if (!await pause(2300, token)) return;
        setState('runRight');
        moveTo(.83, .47, 1300);
        if (!await pause(1350, token)) return;
        setState('waiting');
        announce('roam', 'Sniff zone: all clear.');
        if (!await pause(1600, token)) return;
        setState('runLeft');
        moveTo(.1, .66, 1800);
        if (!await pause(1850, token)) return;
        setState('wave');
        announce('roam', 'Back at base camp.');
        await pause(1300, token);
      }

      if (!valid(token)) return;
      setState('idle');
      currentAction = 'idle';
      announce('idle');
    }

    async function tourLoop(token) {
      const sequence = ['wave', 'zoomies', 'look', 'work', 'roam', 'sleep'];
      while (tourActive && valid(token)) {
        for (const action of sequence) {
          if (!tourActive || !valid(token)) return;
          await runAction(action, token);
          if (!tourActive || !valid(token)) return;
          if (!await pause(650, token)) return;
        }
      }
    }

    const startTour = () => {
      if (reducedMotion) return;
      actionToken += 1;
      tourActive = true;
      updateTourButton();
      tourLoop(actionToken);
    };

    const stopTour = () => {
      actionToken += 1;
      tourActive = false;
      updateTourButton();
      setState('idle');
      announce('idle', 'Tour paused. Pick a trick!');
    };

    const runManualAction = (action) => {
      actionToken += 1;
      tourActive = false;
      updateTourButton();
      runAction(action, actionToken);
    };

    actionButtons.forEach((button) => button.addEventListener('click', () => runManualAction(button.dataset.action)));
    pet.addEventListener('click', () => runManualAction('wave'));
    tourButton.addEventListener('click', () => tourActive ? stopTour() : startTour());
    window.addEventListener('resize', () => {
      if (currentAction === 'idle') moveTo(.12, .62, 0);
    });

    const motionChanged = () => {
      reducedMotion = reducedMotionQuery.matches;
      actionToken += 1;
      tourActive = false;
      animator.refreshForMotionPreference();
      moveTo(.12, .62, 0);
      announce('idle', reducedMotion ? 'Keeping quietly good company.' : 'Motion is back. Play the full tour?');
      updateTourButton();
      if (!reducedMotion) startTour();
    };
    reducedMotionQuery.addEventListener('change', motionChanged);

    moveTo(.12, .62, 0);
    setState('wave');
    updateTourButton();
    if (tourActive) window.setTimeout(() => {
      if (tourActive) startTour();
    }, 500);
  }

  function initAmbientSprites() {
    const deviceElement = document.querySelector('[data-device-sprite]');
    const bubbleElement = document.querySelector('[data-bubble-sprite]');
    const footerElement = document.querySelector('[data-footer-sprite]');
    const animators = [deviceElement, bubbleElement, footerElement]
      .filter(Boolean)
      .map((element) => new SpriteAnimator(element, .5));
    animators.forEach((animator, index) => animator.play(index === 1 ? 'waiting' : index === 2 ? 'wave' : 'idle'));

    const wakeButton = document.querySelector('[data-wake-mobile]');
    const mobileStatus = document.querySelector('[data-mobile-status]');
    if (wakeButton && mobileStatus && animators[1]) {
      wakeButton.addEventListener('click', () => {
        animators[1].play('wave');
        mobileStatus.textContent = 'Kavana is awake';
        wakeButton.textContent = 'Say hi again';
      });
    }

    reducedMotionQuery.addEventListener('change', () => animators.forEach((animator) => animator.refreshForMotionPreference()));
  }

  function initPreviews() {
    const cards = [...document.querySelectorAll('[data-preview]')];
    const playAllButton = document.querySelector('[data-play-all]');
    if (!cards.length || !playAllButton) return;
    let playAll = false;
    const animators = new Map(cards.map((card) => [card, new SpriteAnimator(card.querySelector('.preview-sprite'))]));

    const reset = (card) => {
      animators.get(card).show(card.dataset.previewState);
      card.classList.remove('is-playing');
      card.setAttribute('aria-pressed', 'false');
    };

    const play = (card) => {
      if (reducedMotion) return;
      animators.get(card).play(card.dataset.previewState);
      card.classList.add('is-playing');
      card.setAttribute('aria-pressed', 'true');
    };

    cards.forEach((card) => {
      card.tabIndex = 0;
      card.setAttribute('role', 'button');
      card.setAttribute('aria-pressed', 'false');
      card.addEventListener('pointerenter', () => play(card));
      card.addEventListener('pointerleave', () => { if (!playAll) reset(card); });
      card.addEventListener('focusin', () => play(card));
      card.addEventListener('focusout', () => { if (!playAll) reset(card); });
      card.addEventListener('click', () => play(card));
      card.addEventListener('keydown', (event) => {
        if (event.key !== 'Enter' && event.key !== ' ') return;
        event.preventDefault();
        card.click();
      });
      reset(card);
    });

    const syncPlayAll = () => {
      playAllButton.setAttribute('aria-pressed', String(playAll));
      playAllButton.innerHTML = playAll ? '<span aria-hidden="true">Ⅱ</span> Pause all' : '<span aria-hidden="true">▶</span> Play all';
      cards.forEach((card) => playAll ? play(card) : reset(card));
    };

    playAllButton.addEventListener('click', () => {
      if (reducedMotion) return;
      playAll = !playAll;
      syncPlayAll();
    });

    reducedMotionQuery.addEventListener('change', () => {
      reducedMotion = reducedMotionQuery.matches;
      if (reducedMotion) {
        playAll = false;
        syncPlayAll();
      }
    });
  }

  function initInstallTabs() {
    const tabs = [...document.querySelectorAll('[data-install-tab]')];
    const panels = [...document.querySelectorAll('[data-install-panel]')];
    if (!tabs.length) return;

    const selectTab = (tab, focus = false) => {
      const name = tab.dataset.installTab;
      tabs.forEach((item) => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
      });
      panels.forEach((panel) => { panel.hidden = panel.dataset.installPanel !== name; });
      if (focus) tab.focus();
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => selectTab(tab));
      tab.addEventListener('keydown', (event) => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        let next = index;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        selectTab(tabs[next], true);
      });
    });

    document.querySelectorAll('[data-copy-command]').forEach((button) => {
      button.addEventListener('click', async () => {
        const code = button.closest('[data-install-panel]')?.querySelector('code')?.textContent || '';
        const original = button.textContent;
        try {
          await navigator.clipboard.writeText(code);
          button.textContent = 'Copied!';
        } catch {
          button.textContent = 'Select text';
          button.closest('[data-install-panel]')?.querySelector('pre')?.focus();
        }
        window.setTimeout(() => { button.textContent = original; }, 1800);
      });
    });
  }

  function initReveals() {
    const elements = [...document.querySelectorAll('.reveal')];
    if (reducedMotion || !('IntersectionObserver' in window)) {
      elements.forEach((element) => element.classList.add('is-visible'));
      return;
    }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .1 });
    elements.forEach((element) => observer.observe(element));
  }

  function initMotionNotice() {
    const note = document.querySelector('[data-motion-note]');
    if (!note) return;
    const update = () => { note.hidden = !reducedMotionQuery.matches; };
    update();
    reducedMotionQuery.addEventListener('change', update);
  }

  function init() {
    initHeroPlayground();
    initAmbientSprites();
    initPreviews();
    initInstallTabs();
    initReveals();
    initMotionNotice();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
