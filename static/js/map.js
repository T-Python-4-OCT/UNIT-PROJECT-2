(() => {
  const isEnglish = document.documentElement.lang === 'en';
  const canvas = document.querySelector('#industrial-map-canvas');
  const cities = [...document.querySelectorAll('.city-index-item[data-city-id]')];
  if (!canvas || !cities.length) return;

  const status = document.createElement('div');
  status.className = 'map-load-message';
  status.setAttribute('role', 'status');
  status.textContent = isEnglish ? 'Loading map…' : 'جار تحميل الخريطة الجغرافية…';
  canvas.append(status);

  if (!window.L) {
    status.textContent = isEnglish ? 'Could not load the map library. Check your internet connection.' : 'تعذر تحميل مكتبة الخريطة. تحقق من اتصال الإنترنت.';
    return;
  }

  const map = L.map(canvas, { scrollWheelZoom: false, zoomControl: false }).setView([24, 45], 5);
  map.createPane('city-markers');
  map.getPane('city-markers').style.zIndex = 650;
  L.control.zoom({ position: 'topleft' }).addTo(map);
  let receivedTile = false;
  const tileLayer = L.tileLayer('https://a.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a> · <a href="https://www.openstreetmap.de/">OSM-DE</a>',
  });
  tileLayer.on('tileload', () => {
    receivedTile = true;
    status.remove();
  });
  tileLayer.on('tileerror', () => {
    if (!receivedTile) status.textContent = isEnglish ? 'Could not load map tiles. Check your internet connection.' : 'تعذر تحميل خريطة الأساس. تحقق من اتصال الإنترنت.';
  });
  tileLayer.addTo(map);

  const markers = new Map();
  const regionButtons = [...document.querySelectorAll('.map-region-button[data-region-code]')];
  const regionLayers = new Map();
  let selectedRegion = cities[0]?.dataset.regionCode || '';
  const regionStyle = (code) => {
    const selected = code === selectedRegion;
    return {
      color: selected ? '#bd8a2e' : '#547267',
      weight: selected ? 3 : 1.7,
      opacity: selected ? 1 : 0.88,
      fillColor: selected ? '#d5ad59' : '#789789',
      fillOpacity: selected ? 0.19 : 0.035,
    };
  };
  const selectRegion = (code, moveMap = true) => {
    const button = regionButtons.find((item) => item.dataset.regionCode === code);
    if (!button) return;
    selectedRegion = code;
    regionButtons.forEach((item) => {
      const selected = item.dataset.regionCode === code;
      item.classList.toggle('is-selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    regionLayers.forEach((layer, id) => layer.setStyle(regionStyle(id)));
    regionLayers.forEach((layer, id) => layer.getTooltip()?.getElement()?.classList.toggle('is-selected', id === code));
    if (moveMap) {
      map.flyTo([Number(button.dataset.lat), Number(button.dataset.lon)], Math.max(map.getZoom(), 5.7), { duration: 0.65 });
    }
  };

  const selectCity = (cityId, moveMap = true) => {
    const city = cities.find((item) => item.dataset.cityId === cityId);
    const marker = markers.get(cityId);
    if (!city) return;
    selectRegion(city.dataset.regionCode, false);

    cities.forEach((item) => {
      const selected = item.dataset.cityId === cityId;
      item.classList.toggle('is-selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    markers.forEach((item, id) => {
      const selected = id === cityId;
      item.setStyle(selected
        ? { radius: 12, color: '#183b34', weight: 4, fillColor: '#f1bd44', fillOpacity: 1 }
        : { radius: 9, color: '#fff', weight: 3, fillColor: '#d5a33a', fillOpacity: 1 });
      if (selected) item.openTooltip();
      item.getTooltip()?.getElement()?.classList.toggle('is-selected', selected);
    });

    if (moveMap && marker) {
      map.flyTo(marker.getLatLng(), Math.max(map.getZoom(), 7), { duration: 0.65 });
    }
  };

  cities.forEach((city) => {
    const marker = L.circleMarker([Number(city.dataset.lat), Number(city.dataset.lon)], {
      pane: 'city-markers',
      radius: 9,
      color: '#fff',
      weight: 3,
      fillColor: '#d5a33a',
      fillOpacity: 1,
      bubblingMouseEvents: false,
    }).addTo(map);
    marker.bindTooltip(city.dataset.city, { permanent: true, direction: 'top', offset: [0, -8], className: 'city-map-tooltip', opacity: 1 });
    marker.on('click', () => {
      selectCity(city.dataset.cityId, false);
      window.dispatchEvent(new CustomEvent('industrialmap:select', { detail: { cityId: city.dataset.cityId, updateAddress: true } }));
    });
    markers.set(city.dataset.cityId, marker);
    city.addEventListener('click', () => {
      selectCity(city.dataset.cityId);
      window.dispatchEvent(new CustomEvent('industrialmap:select', { detail: { cityId: city.dataset.cityId, updateAddress: true } }));
    });
  });

  const searchInput = document.querySelector('#map-location-search');
  const sectorFilter = document.querySelector('#map-sector-filter');
  const filterStatus = document.querySelector('#map-filter-status');
  const applyFilters = (zoomToMatches = false) => {
    const query = searchInput.value.trim().toLocaleLowerCase('ar');
    const chosenSector = sectorFilter.value;
    const matches = [];

    cities.forEach((city) => {
      const sectors = city.dataset.sectors.split('|').map((item) => item.trim());
      const searchableText = [city.dataset.city, city.dataset.region, city.dataset.description, ...sectors].join(' ').toLocaleLowerCase('ar');
      const matchesQuery = !query || searchableText.includes(query);
      const matchesSector = !chosenSector || sectors.includes(chosenSector);
      const isMatch = matchesQuery && matchesSector;
      city.classList.toggle('is-filtered-out', !isMatch);

      const marker = markers.get(city.dataset.cityId);
      if (marker) {
        if (isMatch && !map.hasLayer(marker)) marker.addTo(map);
        if (!isMatch && map.hasLayer(marker)) map.removeLayer(marker);
      }
      if (isMatch) matches.push(city);
    });

    if (filterStatus) {
      filterStatus.textContent = isEnglish
        ? (matches.length ? `Showing ${matches.length.toLocaleString('en')} of ${cities.length.toLocaleString('en')} locations. Select one to view its sectors and details.` : 'No locations match your search. Try another activity or city.')
        : (matches.length ? `تظهر ${matches.length.toLocaleString('ar-SA')} من ${cities.length.toLocaleString('ar-SA')} مواقع. اختر موقعاً لعرض القطاعات والمعلومات.` : 'لا توجد مواقع تطابق البحث. جرّب نشاطاً أو مدينة أخرى.');
    }

    const currentSelection = cities.find((city) => city.classList.contains('is-selected'));
    if (matches.length && !matches.includes(currentSelection)) {
      selectCity(matches[0].dataset.cityId, false);
      window.dispatchEvent(new CustomEvent('industrialmap:select', { detail: { cityId: matches[0].dataset.cityId, updateAddress: false } }));
    }

    if (zoomToMatches && matches.length === 1) {
      map.flyTo([Number(matches[0].dataset.lat), Number(matches[0].dataset.lon)], Math.max(map.getZoom(), 7), { duration: 0.65 });
    } else if (zoomToMatches && matches.length > 1) {
      const bounds = L.latLngBounds(matches.map((city) => [Number(city.dataset.lat), Number(city.dataset.lon)]));
      map.flyToBounds(bounds, { padding: [48, 48], maxZoom: 6.2, duration: 0.65 });
    }
  };

  let searchDebounce;
  searchInput?.addEventListener('input', () => {
    window.clearTimeout(searchDebounce);
    searchDebounce = window.setTimeout(() => applyFilters(true), 240);
  });
  sectorFilter?.addEventListener('change', () => applyFilters(true));
  applyFilters(false);

  regionButtons.forEach((button) => button.addEventListener('click', () => selectRegion(button.dataset.regionCode)));

  fetch('/static/geo/saudi-regions.geojson')
    .then((response) => {
      if (!response.ok) throw new Error(`Boundary data returned ${response.status}`);
      return response.json();
    })
    .then((data) => {
      if (data.features?.length !== 13) throw new Error('Expected 13 Saudi administrative regions');
      const boundaries = L.geoJSON(data, {
        style: (feature) => regionStyle(feature.properties.code),
        onEachFeature: (feature, layer) => {
          const { code } = feature.properties;
          const name = isEnglish ? (feature.properties.name_en || feature.properties.name_ar) : feature.properties.name_ar;
          regionLayers.set(code, layer);
          const shortName = isEnglish ? name.replace(/^Region of /, '').replace(/^Region /, '') : name.replace(/^منطقة /, '').replace(/^المنطقة /, '');
          layer.bindTooltip(shortName, { permanent: true, direction: 'center', className: 'region-name-tooltip', opacity: 1 });
          layer.on('click', () => selectRegion(code));
          layer.on('mouseover', () => layer.setStyle({ weight: Math.max(regionStyle(code).weight, 2.5), fillOpacity: 0.13 }));
          layer.on('mouseout', () => layer.setStyle(regionStyle(code)));
        },
      }).addTo(map);
      boundaries.bringToBack();

      selectRegion(selectedRegion, false);
    })
    .catch((error) => console.error('Unable to load Saudi administrative boundaries:', error));

  const initialCity = window.location.hash.slice(1) || cities[0]?.dataset.cityId;
  if (initialCity && markers.has(initialCity)) selectCity(initialCity, false);
  window.requestAnimationFrame(() => window.requestAnimationFrame(() => {
    map.invalidateSize({ pan: false });
    if (window.location.hash && initialCity && markers.has(initialCity)) {
      map.flyTo(markers.get(initialCity).getLatLng(), 7, { duration: 0.65 });
    }
  }));
})();
