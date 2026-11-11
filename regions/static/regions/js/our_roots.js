
document.addEventListener('DOMContentLoaded', () => {
    const root = document.querySelector('.roots-page');
    if (!root) return;

    const current = document.getElementById('roots-journey-current');
    const next = document.getElementById('roots-journey-next');
    const title = document.getElementById('roots-journey-stage-title');
    const description = document.getElementById('roots-journey-stage-description');
    const stamp = document.getElementById('roots-journey-stamp');
    const counter = document.getElementById('roots-journey-counter');
    const stages = [...document.querySelectorAll('.roots-stage')];
    const previousButton = document.getElementById('roots-journey-prev');
    const nextButton = document.getElementById('roots-journey-next-button');

    const sources = [
        current.getAttribute('src'),
        current.getAttribute('src').replace('farm-before.png', 'farm-progress.png'),
        current.getAttribute('src').replace('farm-before.png', 'farm-after.png')
    ];

    const journey = [
        {
            title: 'حين كانت الأرض تنتظر',
            description: 'أرض شبه قاحلة، لا يكسوها إلا القليل من النباتات الطبيعية. هنا بدأت الرؤية الأولى.',
            stamp: 'البداية',
            alt: 'المزرعة قبل الزراعة: أرض شبه قاحلة أمام تل رملي'
        },
        {
            title: 'بدايات الغرس والعناية',
            description: 'بدأت الأشجار الصغيرة تنمو، وظهرت صفوف الغرس وخطوط الري. سنوات من العمل والصبر صنعت الفرق.',
            stamp: 'التحوّل',
            alt: 'بداية تشجير المزرعة بأشجار صغيرة ونظام ري'
        },
        {
            title: 'أرض تنبض بالحياة',
            description: 'بعد خمسة وعشرين عامًا، كبرت الأشجار وأثمرت، وتفتحت الأزهار، وعادت الطيور تحلّق وتتخذ من الأغصان موطنًا.',
            stamp: 'الحاضر',
            alt: 'مزرعة عامرة بأشجار المانجو والزهور والطيور'
        }
    ];

    let active = 0;
    let changing = false;

    sources.forEach(src => {
        const preload = new Image();
        preload.src = src;
    });

    function showStage(index) {
        if (index === active || changing || index < 0 || index >= journey.length) return;

        changing = true;

        const data = journey[index];

        next.src = sources[index];
        next.alt = data.alt;
        next.classList.add('is-visible');

        title.textContent = data.title;
        description.textContent = data.description;
        stamp.textContent = data.stamp;
        counter.textContent = `${String(index + 1).padStart(2, '0')} / 03`;

        stages.forEach((button, i) => {
            const selected = i === index;
            button.classList.toggle('is-active', selected);
            button.setAttribute('aria-pressed', String(selected));
        });

        window.setTimeout(() => {
            current.src = sources[index];
            current.alt = data.alt;
            next.classList.remove('is-visible');
            active = index;
            changing = false;
        }, window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 550);
    }

    stages.forEach(button => {
        button.addEventListener('click', () => {
            showStage(Number(button.dataset.stage));
        });
    });

    previousButton.addEventListener('click', () => {
        showStage((active + journey.length - 1) % journey.length);
    });

    nextButton.addEventListener('click', () => {
        showStage((active + 1) % journey.length);
    });

    const revealElements = document.querySelectorAll('[data-roots-reveal]');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, instance) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-revealed');
                    instance.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        revealElements.forEach(element => observer.observe(element));
    } else {
        revealElements.forEach(element => element.classList.add('is-revealed'));
    }

    const lightbox = document.getElementById('roots-lightbox');
    const lightboxImage = document.getElementById('roots-lightbox-image');
    const lightboxCaption = document.getElementById('roots-lightbox-caption');
    const closeLightboxButton = document.getElementById('roots-lightbox-close');

    let lastFocused = null;

    function closeLightbox() {
        if (lightbox.hidden) return;

        lightbox.hidden = true;
        lightbox.setAttribute('aria-hidden', 'true');

        document.body.classList.remove('roots-modal-open');

        lightboxImage.removeAttribute('src');

        if (lastFocused) {
            lastFocused.focus();
        }
    }

    document.querySelectorAll('[data-lightbox-src]').forEach(button => {
        button.addEventListener('click', () => {
            lastFocused = button;

            lightboxImage.src = button.dataset.lightboxSrc;
            lightboxImage.alt = button.dataset.lightboxAlt || '';
            lightboxCaption.textContent = button.dataset.lightboxAlt || '';

            lightbox.hidden = false;
            lightbox.setAttribute('aria-hidden', 'false');

            document.body.classList.add('roots-modal-open');

            closeLightboxButton.focus();
        });
    });

    closeLightboxButton.addEventListener('click', closeLightbox);

    lightbox.addEventListener('click', event => {
        if (event.target === lightbox) {
            closeLightbox();
        }
    });

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape') {
            closeLightbox();
        }

        if (!lightbox.hidden && event.key === 'Tab') {
            event.preventDefault();
            closeLightboxButton.focus();
        }
    });
});
