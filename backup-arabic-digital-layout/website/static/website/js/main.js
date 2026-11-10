
(function () {
  "use strict";

  var root = document.documentElement;

  
  var themeBtn = document.getElementById("theme-toggle");
  var themeLabel = document.getElementById("theme-label");
  var themeColor = document.querySelector('meta[name="theme-color"]');

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var isDark = theme === "dark";
    if (themeBtn) themeBtn.setAttribute("aria-pressed", String(isDark));
    if (themeLabel && themeBtn) themeLabel.textContent = themeBtn.getAttribute(isDark ? "data-label-on-dark" : "data-label-on-light");
    if (themeBtn) themeBtn.setAttribute("aria-label", themeBtn.getAttribute(isDark ? "data-aria-on-dark" : "data-aria-on-light"));
    if (themeColor) themeColor.setAttribute("content", isDark ? "#0D122C" : "#16644A");
  }

  applyTheme(root.getAttribute("data-theme") || "light");

  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      try { localStorage.setItem("theme", next); } catch (e) {  }
    });
  }

  
  var menuBtn = document.getElementById("menu-toggle");
  var nav = document.getElementById("site-nav");

  function setMenu(open) {
    document.body.classList.toggle("nav-open", open);
    if (menuBtn) {
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.setAttribute("aria-label", menuBtn.getAttribute(open ? "data-label-open" : "data-label-closed"));
    }
  }

  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      setMenu(!document.body.classList.contains("nav-open"));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
  }

  
  document.addEventListener("click", function (e) {
    var link = e.target.closest("a[href]");
    if (!link) return;
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (link.target && link.target !== "_self") return;
    if (link.hasAttribute("download")) return;

    var url;
    try { url = new URL(link.href, window.location.href); } catch (err) { return; }
    if (url.origin !== window.location.origin) return;
    if (url.pathname === window.location.pathname && url.search === window.location.search) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    e.preventDefault();
    document.body.classList.add("is-leaving");
    window.setTimeout(function () { window.location.href = url.href; }, 180);
  });
  window.addEventListener("pageshow", function () {
    document.body.classList.remove("is-leaving");
  });

  
  var chips = document.querySelectorAll(".chip[data-filter]");
  var cards = document.querySelectorAll("#gallery .card");

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var filter = chip.getAttribute("data-filter");
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
      cards.forEach(function (card) {
        var show = filter === "all" || card.getAttribute("data-kind") === filter;
        card.hidden = !show;
      });
    });
  });


  // The language choice is shared by every route and survives internal navigation.
  var languageButton = document.getElementById("language-toggle");
  var translations = {
    "انتقل إلى المحتوى":"Skip to content", "التصميم السعودي":"Saudi Design", "الرئيسية":"Home", "الهوية والتراث":"Identity & Heritage", "التصميم الرقمي":"Digital Design", "العمارة":"Architecture", "الجرافيك":"Graphic Design", "المنتجات والأزياء":"Products & Fashion", "المعاصر":"Contemporary",
    "تصفّح المجالات":"Explore disciplines", "ابدأ رحلتك":"Start your journey", "اكتشف عناصر الهوية السعودية وكيف تتحول إلى عمارة وتصميم ومنتجات وتجارب رقمية.":"Explore Saudi identity and its expression in architecture, design, products and digital experiences.", "تعرّف على السدو والقط العسيري والعمارة السعودية، ثم شاهد أثرها في التصميم المعاصر.":"Discover Al Sadu, Al-Qatt Al-Asiri and Saudi architecture, then see how they inspire contemporary design.", "استكشف الهوية والتراث":"Explore identity & heritage", "اكتشف التصميم الرقمي":"Discover digital design",
    "الوضع الليلي":"Dark mode", "الوضع النهاري":"Light mode", "فتح القائمة":"Open menu", "إغلاق القائمة":"Close menu",
    "تصميم المنتجات والأزياء والديكور":"Product, Fashion & Interior Design", "تراث يُلمس باليد":"Heritage you can touch", "يربط تصميم المنتج بين الاستخدام اليومي والخامة المحلية والهوية البصرية.":"Product design connects everyday use with local materials and visual identity.", "من الأثاث إلى التغليف، يوازن التصميم الناجح بين الوظيفة والجمال وسهولة الاستخدام.":"From furniture to packaging, successful design balances function, beauty and ease of use.", "قطع تعيش في البيت يوميًا":"Pieces for everyday living", "المنتجات والأثاث":"Products & Furniture", "أثاث وإضاءة وإكسسوارات بخامات محلية وتفاصيل معاصرة.":"Furniture, lighting and accessories using local materials and contemporary details.", "أفكار تصميمية":"Design ideas", "جلسات أرضية ومجالس بتفاصيل حديثة.":"Floor seating and majlis with modern details.", "إضاءة مستلهمة من الفتحات الهندسية.":"Lighting inspired by geometric openings.", "قطع من الخوص والنسيج المحلي.":"Pieces made with local palm weaving and textiles.", "فضاء يحكي مكانه":"A space rooted in place", "التصميم الداخلي":"Interior Design", "تربط الأخشاب والزخارف والألوان المحلية المساحة بهويتها.":"Local wood, patterns and colors connect a space to its identity.", "حواجز خشبية مخرّمة تشبه الرواشين.":"Carved wooden screens inspired by rawasheen.", "أشرطة زخرفية هندسية على الجدران.":"Geometric decorative bands on walls.", "ألوان ترابية بلمسات دافئة.":"Earthy colors with warm accents.", "قماش وقصّة وهوية":"Fabric, form and identity", "الأزياء والملابس":"Fashion & Clothing", "توظّف الأزياء المعاصرة النقوش والخامات المحلية في قصّات جديدة.":"Contemporary fashion brings local patterns and materials into new silhouettes.", "أقمشة بنقوش مستوحاة من السدو.":"Textiles patterned after Al Sadu.", "تطريز بأشكال هندسية.":"Embroidery with geometric forms.", "قصّات حديثة بعناصر تقليدية.":"Modern silhouettes with traditional elements.", "الانطباع الأول بين اليدين":"A first impression in hand", "العبوات والتغليف":"Packaging", "يجمع التغليف الواضح بين المعلومات وهوية المنتج.":"Clear packaging brings product information together with brand identity.", "نقوش هندسية مختزلة.":"Simplified geometric patterns.", "خط عربي سهل القراءة.":"Legible Arabic typography.", "مواد قابلة لإعادة الاستخدام أو التدوير.":"Reusable or recyclable materials.", "الخامة أول عناصر الهوية":"Material as the first expression of identity", "المواد المحلية والاستدامة":"Local Materials & Sustainability", "يربط الخوص والصوف والحجر المنتج ببيئته وموارده.":"Palm weaving, wool and stone connect products to local resources.", "الخوص للديكور والتغليف.":"Palm weaving for décor and packaging.", "الصوف والنسيج للمفروشات.":"Wool and textiles for furnishings.", "الطين والحجر للأثاث الخارجي.":"Clay and stone for outdoor furniture.", "مبادرات وتجارب محلية":"Local initiatives and experiences", "مشاريع تفتح مساحة للمصممين والمنتجات السعودية.":"Projects creating opportunities for Saudi designers and products.",
    "التصميم المعاصر والمشاريع السعودية":"Contemporary Design & Saudi Projects", "ما يُصنع اليوم في السعودية":"Made in Saudi today", "معارض ومهرجانات ومبادرات تدعم قطاع التصميم وتجمع بين التراث والابتكار.":"Exhibitions, festivals and initiatives supporting design and bringing heritage together with innovation.", "معرض الفعاليات والمبادرات":"Events & initiatives", "تدعم هيئة فنون العمارة والتصميم نمو القطاع، وتعرض الفعاليات أفكارًا ومنتجات جديدة. اختر تصنيفًا لتصفية البطاقات.":"The Architecture and Design Commission supports the sector through events featuring new ideas and products. Choose a category to filter.", "الكل":"All", "فعالية":"Event", "معرض":"Exhibition", "مبادرة":"Initiative", "اعتراف دولي":"International recognition", "معرض دولي":"International exhibition", "الرياض، 2022 و2023":"Riyadh, 2022 and 2023", "مهرجان التصميم السعودي":"Saudi Design Festival", "معارض ومنتدى وورش وسوق للتصميم في حي جاكس.":"Exhibitions, a forum, workshops and a design market in JAX District.", "قدّمت هيئة فنون العمارة والتصميم النسخة الأولى في يناير 2022، وتلتها نسخة ثانية في يناير 2023.":"The Architecture and Design Commission presented the first edition in January 2022, followed by a second in January 2023.", "داون تاون ديزاين الرياض":"Downtown Design Riyadh", "الرياض مدينة مبدعة للتصميم":"Riyadh, a UNESCO Creative City of Design", "انضمت الرياض إلى شبكة اليونسكو للمدن المبدعة في مجال التصميم.":"Riyadh joined the UNESCO Creative Cities Network in the field of Design.", "يربط هذا الاعتراف التصميم بتطوير المدينة، من المساحات العامة إلى التجارب الثقافية اليومية.":"This recognition links design with city development, from public spaces to everyday cultural experiences.", "الاستدامة والمواد المحلية":"Sustainability & local materials", "مشاريع تجمع التراث والابتكار":"Projects bringing heritage and innovation together",
    "العمارة والتصميم الحضري":"Architecture & Urban Design", "من الطين إلى الأبراج":"From clay homes to skyscrapers", "العمارة السعودية تستجيب للمناخ بمواد محلية وتفاصيل عملية، من البيوت القديمة إلى أحياء اليوم.":"Saudi architecture responds to climate through local materials and practical details, from historic homes to today's districts.", "طرازان تقليديان":"Two traditional styles", "أساليب معمارية صاغها المكان والمواد المتاحة.":"Architectural traditions shaped by place and available materials.", "بنية تحمي من الحرارة":"A structure shaped by the climate", "العمارة النجدية":"Najdi Architecture", "الطين واللبن مع جذوع النخل في الأسقف.":"Mud brick and palm trunks in roof structures.", "جدران سميكة وفتحات صغيرة.":"Thick walls and small openings.", "فناء داخلي للضوء والتهوية.":"An inner courtyard for light and ventilation.", "شرفات مثلثة تتوّج الجدران.":"Triangular parapets crown the walls.", "مثال: حي الطريف في الدرعية.":"Example: At-Turaif District in Diriyah.", "واجهات تتنفس":"Breathing façades", "العمارة الحجازية":"Hejaz Architecture", "الحجر المنقبي والخشب.":"Coral stone and wood.", "رواشين بارزة للتهوية والخصوصية.":"Projecting rawasheen provide ventilation and privacy.", "بيوت متعددة الطوابق.":"Multi-storey homes.", "واجهات خشبية منقوشة.":"Carved wooden façades.", "مثال: جدة التاريخية.":"Example: Historic Jeddah.", "معالم ومشاريع عمرانية":"Landmarks & urban projects", "مواقع تراثية ومشاريع حديثة في مدن المملكة.":"Heritage sites and contemporary projects across Saudi cities.",
    "الهوية والتراث السعودي":"Saudi Identity & Heritage", "نقوش تحكي من نحن":"Patterns that tell our story", "السدو والقط العسيري والخط العربي والعمارة الإقليمية عناصر تشكّل لغة بصرية سعودية.":"Al Sadu, Al-Qatt Al-Asiri, Arabic calligraphy and regional architecture shape a Saudi visual language.", "مفردات من التراث البصري":"Elements of visual heritage", "حرف وخامات وأشكال ما زالت تلهم التصميم اليوم.":"Crafts, materials and forms that continue to inspire design today.", "الطرز الإقليمية":"Regional architectural styles", "ألوان من البيئة":"Colors of the landscape", "استلهام يحترم الأصل":"Inspiration with respect for its roots", "شاهد كيف يُنسج السدو":"Watch how Al Sadu is woven", "حرفة حيّة · فيلم توثيقي":"Living craft · Documentary", "يوضح الفيلم مراحل الحياكة على النول الأرضي، ويقرّب تفاصيل حركة الخيوط التي لا تظهر في الصورة الثابتة.":"This film shows weaving on a ground loom and reveals the movement of threads that a still image cannot capture.", "بطاقة السدو لدى اليونسكو":"UNESCO Al Sadu listing", "الفيلم من جمعية المحافظة على التراث في السعودية، 2019.":"Film by the Saudi Heritage Preservation Society, 2019.", "افهم السياق":"Understand the context", "اختزل الفكرة":"Distill the idea", "صمّم لوظيفة":"Design for a purpose",
    "هوية واحدة، مجالات متعددة":"One identity, many disciplines", "من الجذور إلى المستقبل":"From roots to the future", "تعرّف على العناصر التي تصنع لغة التصميم في المملكة، من الحرف والعمارة إلى العلامات والخدمات الرقمية.":"Discover the elements shaping design in Saudi Arabia, from crafts and architecture to brands and digital services.", "ابدأ من الهوية والتراث":"Start with identity & heritage", "استكشف المجالات":"Explore disciplines", "التصميم السعودي حوار مستمر بين المكان والناس. استكشف مفرداته، ثم شاهد كيف تظهر في المباني والمنتجات والهويات والتجارب التي نستخدمها كل يوم.":"Saudi design is an ongoing dialogue between place and people. Explore its vocabulary and see how it appears in buildings, products, identities and everyday experiences.", "تصفّح مجالات التصميم":"Explore design disciplines", "اختر مجالاً لتتعرف على لغته البصرية وأمثلة من المملكة.":"Choose a discipline to explore its visual language and examples from Saudi Arabia.", "الجذور البصرية":"Visual roots", "السدو والقط العسيري والخط والحرف المحلية.":"Al Sadu, Al-Qatt Al-Asiri, calligraphy and local crafts.", "المكان والمناخ":"Place and climate", "مواد وأساليب معمارية من البيوت التاريخية إلى المدن الحديثة.":"Architectural materials and traditions, from historic homes to modern cities.", "حرف وشكل ولون":"Type, form and color", "كيف تتآلف العلامة والخط والزخرفة في رسالة واحدة.":"How identity, typography and pattern work together in one message.", "تجربة واضحة":"A clear experience", "مكوّنات موحّدة تجعل الخدمات أسهل في الاستخدام.":"Consistent components make services easier to use.", "من الفكرة إلى الاستخدام":"From idea to use", "أشياء تجمع الوظيفة والخامة والهوية المحلية.":"Objects that combine function, material and local identity.", "ما يُصنع اليوم":"Made today", "معارض ومبادرات ومشاريع تجمع التراث بالابتكار.":"Exhibitions, initiatives and projects bringing heritage together with innovation.", "من التراث إلى التجربة اليومية":"From heritage to everyday experience", "تظهر الهوية حين تتحول إلى قرارات تصميمية مفهومة ومفيدة.":"Identity comes to life through clear and useful design decisions.", "افهم المكان والحرفة":"Understand place and craft", "ابدأ بالمواد والمناخ والمعنى الذي يحمله العنصر التراثي.":"Begin with materials, climate and the meaning carried by a heritage element.", "صمّم لاحتياج معاصر":"Design for a contemporary need", "حوّل ما تعلّمته إلى شكل أو خدمة أو منتج يؤدي وظيفة واضحة.":"Turn what you learn into a form, service or product with a clear purpose.", "اكتشف مفردات الهوية السعودية":"Discover Saudi identity", "شاهد كيف تلهم الحرف والألوان والعمارة لغة تصميم تنتمي إلى المكان.":"See how crafts, colors and architecture inspire a design language rooted in place.", "شاهد التصميم المعاصر":"Explore contemporary design",
    "ما الذي يجعل الخدمة واضحة؟":"What makes a service clear?", "تصميم رقمي جيد يقلل الحيرة ويجعل الخطوات متوقعة.":"Good digital design reduces uncertainty and makes each step predictable.", "خطوات واضحة":"Clear steps", "يعرف المستخدم أين يبدأ وكيف ينهي طلبه.":"Users know where to start and how to complete a request.", "تنقّل مفهوم":"Intuitive navigation", "تعمل الواجهة بوضوح على الهاتف والحاسب.":"The interface works clearly on mobile and desktop.", "عناصر متسقة":"Consistent elements", "للأزرار والنماذج شكل وسلوك مألوف.":"Buttons and forms have familiar appearances and behaviors.", "وصول للجميع":"Accessible to everyone", "تباين وقراءة وتنقّل يناسب احتياجات مختلفة.":"Contrast, readability and navigation support different needs.", "كود المنصات":"Platform Design System", "نظام تصميم موحّد لواجهات الخدمات الحكومية في المملكة.":"A unified design system for government service interfaces across Saudi Arabia.", "ما الفائدة؟":"Why it matters", "شكل موحّد يسهل التعرّف على الخدمات.":"A consistent look makes services easier to recognize.", "مكوّنات جاهزة تختصر وقت بناء الواجهات.":"Ready-made components speed up interface development.", "تجربة أوضح عبر الأجهزة والصفحات.":"A clearer experience across devices and pages.", "معلومات أساسية":"Key information", "هيئة الحكومة الرقمية":"Digital Government Authority", "الألوان والخط والمكوّنات":"Color, type and components", "مثال على واجهة موحّدة":"A unified interface example",
    "مجالات التصميم الجرافيكي":"Graphic design disciplines", "كل عنصر بصري يؤدي وظيفة في توصيل الفكرة.":"Every visual element helps communicate an idea.", "الشعارات":"Logos", "الهويات البصرية":"Visual identities", "الملصقات":"Posters", "المطبوعات":"Print", "الخط والزخارف":"Typography and patterns",
    "الرياض، 2025":"Riyadh, 2025", "مبادرة تسلط الضوء على مصممي المنتجات الناشئين.":"An initiative spotlighting emerging product designers.", "تدعم ظهور المنتجات السعودية، وتفتح فرص العرض والتعاون والتجريب مع الجامعات.":"It raises the profile of Saudi products and creates opportunities to exhibit, collaborate and experiment with universities.", "معرض تصميم عُقد في حي جاكس بالتعاون مع هيئة فنون العمارة والتصميم.":"A design exhibition held in JAX District with the Architecture and Design Commission.", "جمع المعرض علامات ومصممين ومنتجات في مساحة واحدة من 20 إلى 23 مايو 2025.":"The exhibition brought brands, designers and products together from 20 to 23 May 2025.", "مشاركة إثراء في أسبوع ميلانو للتصميم.":"Ithra's participation in Milan Design Week.", "يعرض البرنامج التصميم والثقافة السعودية، ويعرّف الجمهور بمركز إثراء في الظهران.":"The program presents Saudi design and culture and introduces audiences to Ithra in Dhahran.", "نسيج محلي يحمل اللون والنمط إلى المنتجات.":"A local textile bringing color and pattern into products.", "تمنح وحداته المتكررة الأقمشة والعبوات هوية مميزة عند تبسيطها.":"Its repeated motifs give textiles and packaging a distinctive identity when simplified.", "سعف النخل مادة متجددة للحرف والديكور.":"Palm fronds are a renewable material for crafts and décor.", "تُصنع منه السلال والحصر، ويمكن استخدامه في منتجات وعبوات قابلة لإعادة الاستخدام.":"They are woven into baskets and mats, and can be used in reusable products and packaging.", "خامة محلية تظهر بوضوح في مباني الدرعية التاريخية.":"A local material clearly visible in Diriyah's historic buildings.", "استخدام التربة والمواد المتاحة محليًا شكّل واجهات بملمس ولون مرتبطين بالمكان.":"Local earth and materials shaped façades with textures and colors rooted in place.", "الدرعية وحي الطريف":"Diriyah and At-Turaif District", "الدرعية، الرياض":"Diriyah, Riyadh", "مقر حكم الدولة السعودية الأولى، ومثال بارز للعمارة النجدية بالطين والأفنية الداخلية.":"The seat of the First Saudi State and a prominent example of Najdi mud architecture and inner courtyards.", "أُدرج في قائمة التراث العالمي عام 2010":"Inscribed on the World Heritage List in 2010", "من معالمه قصر سلوى":"Notable landmark: Salwa Palace", "جدة التاريخية":"Historic Jeddah", "ميناء تاريخي يضم بيوتًا متعددة الطوابق مبنية بالحجر المنقبي والخشب.":"A historic port with multi-storey homes built from coral stone and wood.", "أُدرجت عام 2014":"Inscribed in 2014", "تشتهر بالرواشين":"Known for its rawasheen", "مقابر منحوتة في صخور الحِجر":"Tombs carved into the rocks of Hegra", "مقابر نبطية منحوتة في الصخر الرملي؛ مثال على اندماج العمارة بالطبيعة.":"Nabataean tombs carved into sandstone, showing architecture integrated with nature.", "أول موقع سعودي في القائمة عام 2008":"Saudi Arabia's first site on the list, in 2008", "خامة الموقع: الحجر الرملي":"Site material: sandstone", "مركز الملك عبدالله المالي":"King Abdullah Financial District", "حي أعمال متعدد الاستخدامات يجمع الأبراج والمساحات العامة ومحطة مترو.":"A mixed-use business district bringing together towers, public spaces and a metro station.", "المخطط العام: هنينغ لارسن":"Master plan: Henning Larsen", "محطة المترو: زها حديد للعمارة":"Metro station: Zaha Hadid Architects", "محطات متبادلة صُمّمت لتكون جزءًا واضحًا ومريحًا من تجربة التنقل اليومية.":"Interchange stations designed as a clear and comfortable part of everyday travel.", "قصر الحكم: سنوهيتا":"Qasr Al Hokm: Snøhetta", "محطة كافد: زها حديد للعمارة":"KAFD station: Zaha Hadid Architects", "من معالمه قصر سلوى":"Notable landmark: Salwa Palace", "تراث عالمي":"World Heritage", "عمارة معاصرة":"Contemporary architecture", "تصميم حضري":"Urban design", "تراث":"Heritage", "فعالية":"Event", "معرض دولي · ميلانو":"International exhibition · Milan", "مبادرة · المملكة":"Initiative · Saudi Arabia", "حرفة تقليدية · أنحاء المملكة":"Traditional craft · Saudi Arabia", "الطرز الإقليمية":"Regional styles", "مواد وأساليب تشكّلت بحسب المكان والمناخ.":"Materials and traditions shaped by place and climate.", "وسط المملكة":"Central Saudi Arabia", "الساحل الغربي":"Western coast", "جنوب غرب المملكة":"Southwestern Saudi Arabia", "المواد:":"Materials:", "أخضر النخيل":"Palm green", "رمل":"Sand", "طين":"Clay", "أحمر السدو":"Al Sadu red", "عسلي":"Amber", "حجر":"Stone", "النخل والواحات":"Palms and oases", "الكثبان والسهول":"Dunes and plains", "العمارة النجدية":"Najdi architecture", "خيوط النسيج":"Textile threads", "ألوان السدو الدافئة":"Warm Al Sadu colors", "بيوت الحجاز وعسير":"Homes of the Hejaz and Asir", "ثلاث خطوات عملية لاستخدام التراث في تصميم جديد.":"Three practical steps for bringing heritage into new design.", "تعرّف على المنطقة والحرفة ومعنى العنصر قبل توظيفه.":"Learn about the region, craft and meaning before using an element.", "استلهم الشكل والإيقاع بدل نسخ النقش كما هو.":"Take inspiration from form and rhythm instead of copying a pattern.", "حوّل الخامة والتظليل والفناء إلى حلول عملية.":"Turn material, shade and courtyard principles into practical solutions.", "مهرجان التصميم السعودي":"Saudi Design Festival", "داون تاون ديزاين الرياض":"Downtown Design Riyadh", "Designed in Saudi":"Designed in Saudi", "مجموعات جسور للتصميم":"Jusoor Design Collections", "أسبوع إثراء للتصميم":"Ithra Design Week", "الرياض":"Riyadh", "المملكة":"Saudi Arabia", "منصة تبرز مواهب تصميم المنتجات الناشئة، وتدعم فرص العرض والتعاون والتجريب مع الجامعات.":"A platform showcasing emerging product designers and supporting opportunities to exhibit, collaborate and experiment with universities.", "عرض يقدم مصممين سعوديين ومنتجات وتجارب محلية لجمهور أسبوع ميلانو للتصميم.":"A showcase introducing Saudi designers, products and local experiences to Milan Design Week audiences.",
    "تصميم المدن والمساحات العامة":"City and public-space design", "الشوارع والساحات والحدائق ومسارات المشاة تكمل تجربة المباني.":"Streets, plazas, parks and walking routes complete the experience of buildings.", "المساحات العامة":"Public spaces", "أماكن للجلوس والتجمع مع ظل وتهوية تناسب المناخ.":"Places to sit and gather, with shade and ventilation suited to the climate.", "الحدائق والممرات":"Parks and walkways", "مسارات مشي متصلة تربط الأحياء بالمحطات والخدمات.":"Connected walking routes link neighborhoods with stations and services.", "اللوحات الإرشادية":"Wayfinding", "خطوط وألوان ورموز تجعل الوصول أسهل للمقيم والزائر.":"Type, colors and symbols make navigation easier for residents and visitors.", "مبادئ تستفيد من التراث":"Principles inspired by heritage", "استلهم من المناخ":"Learn from the climate", "الأفنية والتظليل حلول قديمة تناسب مباني اليوم.":"Courtyards and shade are time-tested solutions for today's buildings.", "أحيِ المكان":"Bring places to life", "اجمع حفظ الأصل مع الثقافة والزيارة والاستخدام العام.":"Bring conservation together with culture, visits and public use.", "أظهر الخامة":"Celebrate the material", "استخدم الطين والحجر والخشب بصدق بدل تقليدها.":"Use clay, stone and wood honestly instead of imitating them."
  };
  var originalTitle = document.title;
  var reverseTranslations = {}; Object.keys(translations).forEach(function (key) { reverseTranslations[translations[key]] = key; });
  function applyLanguage(language) {
    var english = language === "en";
    root.setAttribute("lang", english ? "en" : "ar");
    root.setAttribute("dir", english ? "ltr" : "rtl");
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      var node = walker.currentNode;
      var key = node.nodeValue.trim();
      var translated = english ? translations[key] : reverseTranslations[key];
      if (translated) node.nodeValue = node.nodeValue.replace(key, translated);
    }
    if (languageButton) languageButton.textContent = english ? "العربية" : "English";
    if (languageButton) languageButton.setAttribute("aria-label", english ? "التبديل إلى العربية" : "Switch language to English");
    var themeButton = document.getElementById("theme-toggle");
    if (themeButton) { themeButton.setAttribute("data-label-on-dark", english ? "Light mode" : "الوضع النهاري"); themeButton.setAttribute("data-label-on-light", english ? "Dark mode" : "الوضع الليلي"); themeButton.setAttribute("data-aria-on-dark", english ? "Light mode" : "الوضع النهاري"); themeButton.setAttribute("data-aria-on-light", english ? "Dark mode" : "الوضع الليلي"); }
    var menuButton = document.getElementById("menu-toggle");
    if (menuButton) { menuButton.setAttribute("data-label-open", english ? "Close menu" : "إغلاق القائمة"); menuButton.setAttribute("data-label-closed", english ? "Open menu" : "فتح القائمة"); menuButton.setAttribute("aria-label", english ? "Open menu" : "فتح القائمة"); }
    ["alt", "aria-label", "title", "placeholder"].forEach(function (attribute) { document.querySelectorAll("[" + attribute + "]").forEach(function (element) { var value = element.getAttribute(attribute); var replacement = english ? translations[value] : reverseTranslations[value]; if (replacement) element.setAttribute(attribute, replacement); }); });
    document.title = english ? (translations[originalTitle.split(" | ")[0]] || originalTitle) : originalTitle;
    try { localStorage.setItem("site-language", language); } catch (e) {}
  }
  if (languageButton) {
    languageButton.addEventListener("click", function () { applyLanguage(root.getAttribute("lang") === "ar" ? "en" : "ar"); });
    try { applyLanguage(localStorage.getItem("site-language") || "ar"); } catch (e) { applyLanguage("ar"); }
  }
})();
