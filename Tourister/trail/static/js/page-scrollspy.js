(() => {
  const nav = document.querySelector(".nt-primary-nav");
  if (!nav) return;

  const links = Array.from(nav.querySelectorAll("a[data-scrollspy]"));
  const pageLinks = links
    .map((link) => {
      const target = new URL(link.href, window.location.href);
      if (target.pathname !== window.location.pathname || !target.hash) return null;

      const id = decodeURIComponent(target.hash.slice(1));
      const section = document.getElementById(id);
      return section ? { link, section } : null;
    })
    .filter(Boolean);
  const sections = pageLinks.map(({ section }) => section);

  if (!sections.length) return;

  let scheduled = false;

  const updateActiveLink = () => {
    scheduled = false;
    const siteNav = document.querySelector(".nt-navbar");
    const activationLine = (siteNav?.getBoundingClientRect().height || 0) + 12;

    let activeSection = sections[0];
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= activationLine) {
        activeSection = section;
      } else {
        break;
      }
    }

    if (
      window.innerHeight + window.scrollY >=
      document.documentElement.scrollHeight - 2
    ) {
      activeSection = sections[sections.length - 1];
    }

    for (const { link, section } of pageLinks) {
      const isActive = section === activeSection;
      link.classList.toggle("active", isActive);
      if (isActive) {
        link.setAttribute("aria-current", "location");
      } else {
        link.removeAttribute("aria-current");
      }
    }
  };

  const scheduleUpdate = () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(updateActiveLink);
  };

  window.addEventListener("scroll", scheduleUpdate, { passive: true });
  window.addEventListener("resize", scheduleUpdate);
  window.addEventListener("hashchange", scheduleUpdate);
  scheduleUpdate();
})();
