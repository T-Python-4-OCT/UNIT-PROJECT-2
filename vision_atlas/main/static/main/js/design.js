const navbar = document.querySelector('.navbar');

if (document.body.classList.contains('has-hero')) {
    const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 50);
    onScroll();
    window.addEventListener('scroll', onScroll);
}

document.body.classList.add('js-reveal');

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.15 });

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

const steps = document.querySelectorAll('.scrolly-step');

if (steps.length) {
    const images = document.querySelectorAll('.scrolly-img');

    const stepObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            const current = entry.target.dataset.step;
            steps.forEach((s) => s.classList.toggle('active', s === entry.target));
            images.forEach((img) => img.classList.toggle('active', img.dataset.step === current));
        });
    }, { rootMargin: '-45% 0px -45% 0px' });

    steps.forEach((s) => stepObserver.observe(s));
}


document.querySelectorAll('.stat-value').forEach((el) => {
    const match = el.textContent.trim().match(/^([\d,]+)(.*)$/);
    if (!match) return;

    const [, numberText, suffix] = match;
    if (!numberText.includes(',') && !suffix) return;

    const target = parseInt(numberText.replace(/,/g, ''), 10);
    const start = performance.now();
    const duration = 3500;

    function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(target * eased).toLocaleString('en-US') + suffix;
        if (progress < 1) requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
});


const progressBar = document.querySelector('.scroll-progress');

function updateProgress() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const progress = max > 0 ? window.scrollY / max : 0;
    progressBar.style.width = `${progress * 100}%`;
}

updateProgress();
window.addEventListener('scroll', updateProgress);

const slider = document.querySelector('.slider');

if (slider) {
    document.querySelectorAll('.slider-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
            const step = slider.querySelector('.slide').offsetWidth + 20;
            slider.scrollBy({ left: step * Number(btn.dataset.dir) });
        });
    });
}


const countdown = document.querySelector('.countdown');

if (countdown) {
    const target = new Date(countdown.dataset.target);
    const units = {
        days: countdown.querySelector('[data-unit="days"]'),
        hours: countdown.querySelector('[data-unit="hours"]'),
        minutes: countdown.querySelector('[data-unit="minutes"]'),
        seconds: countdown.querySelector('[data-unit="seconds"]'),
    };

    function updateCountdown() {
        const diff = Math.max(0, target - new Date());
        units.days.textContent = Math.floor(diff / 86400000);
        units.hours.textContent = Math.floor(diff / 3600000) % 24;
        units.minutes.textContent = Math.floor(diff / 60000) % 60;
        units.seconds.textContent = Math.floor(diff / 1000) % 60;
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);
}

const mapEl = document.getElementById('vision-map');

if (mapEl && window.maplibregl) {
    const projects = JSON.parse(document.getElementById('map-data').textContent);
    const isTouch = window.matchMedia('(pointer: coarse)').matches;

    const homeView = { center: [43.5, 24.5], zoom: 5.1, pitch: 50, bearing: -12 };

    maplibregl.setRTLTextPlugin('https://unpkg.com/@mapbox/mapbox-gl-rtl-text@0.3.0/dist/mapbox-gl-rtl-text.js', true);

    const map = new maplibregl.Map({
        container: mapEl,
        style: 'https://tiles.openfreemap.org/styles/liberty',
        ...homeView,
        cooperativeGestures: isTouch,
        scrollZoom: false,
        attributionControl: { compact: true },
    });

    map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }));

    class ResetControl {
        onAdd() {
            const box = document.createElement('div');
            box.className = 'maplibregl-ctrl maplibregl-ctrl-group';
            box.innerHTML = '<button type="button" title="Reset view"><i class="bi bi-globe2"></i></button>';
            box.querySelector('button').addEventListener('click', () => {
                map.flyTo({ ...homeView, duration: 2000, essential: true });
            });
            return box;
        }

        onRemove() {}
    }

    map.addControl(new ResetControl());

    projects.forEach((p, i) => {
        const lngLat = [p.coords[1], p.coords[0]];

        const el = document.createElement('div');
        el.className = 'map-pin';
        el.innerHTML = `<span>${String(i + 1).padStart(2, '0')}</span>`;

        const stats = p.stats
            .map((s) => `<div><strong>${s.value}</strong><small>${s.label}</small></div>`)
            .join('');

        const popup = new maplibregl.Popup({ offset: 24, maxWidth: '280px', anchor: 'bottom' }).setHTML(`
            <div class="map-popup">
                <img src="${p.image}" alt="${p.name}">
                <div class="map-popup-body">
                    <h3>${p.name}</h3>
                    <p>${p.tagline}</p>
                    <div class="map-popup-stats">${stats}</div>
                    <a href="${p.url}" class="btn btn-success btn-sm rounded-pill px-3">${mapEl.dataset.explore}</a>
                </div>
            </div>`);

        new maplibregl.Marker({ element: el })
            .setLngLat(lngLat)
            .setPopup(popup)
            .addTo(map);

        el.addEventListener('click', () => {
            map.flyTo({
                center: lngLat,
                zoom: 9,
                pitch: 60,
                bearing: map.getBearing() + 30,
                offset: [0, 170],
                duration: 2500,
                essential: true,
            });
        });
    });
}