// Sample Products Data - Replace with your AliExpress affiliate links
const USD_TO_DZD = 135;
let products = [];

const deals = [
    {
        id: 101,
        title: "عرض محدود - مجموعة المنزل الذكي",
        image: "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=600",
        badge: "خصم 60%",
        price: 49.99,
        originalPrice: 129.99,
        endsIn: 86400 * 2 + 3600 * 5
    },
    {
        id: 102,
        title: "مجموعة الصيف - عروض الأزياء",
        image: "https://images.unsplash.com/photo-1445205170230-053b83016050?w=600",
        badge: "خصم 45%",
        price: 29.99,
        originalPrice: 54.99,
        endsIn: 86400 + 3600 * 12
    },
    {
        id: 103,
        title: "تخفيضات كبيرة على الأجهزة التقنية",
        image: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600",
        badge: "خصم 70%",
        price: 19.99,
        originalPrice: 66.99,
        endsIn: 3600 * 8 + 1800
    },
    {
        id: 104,
        title: "سماعات لاسلكية برو ماكس",
        image: "https://images.unsplash.com/photo-1590658268037-6bf12f032f55?w=600",
        badge: "خصم 55%",
        price: 15.99,
        originalPrice: 35.99,
        endsIn: 86400 * 3 + 3600 * 2
    },
    {
        id: 105,
        title: "ساعة ذكية رياضية متقدمة",
        image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600",
        badge: "خصم 50%",
        price: 24.99,
        originalPrice: 49.99,
        endsIn: 86400 + 3600 * 6
    },
    {
        id: 106,
        title: "شاحن لاسلكي أنيق 3 في 1",
        image: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600",
        badge: "خصم 40%",
        price: 12.99,
        originalPrice: 21.99,
        endsIn: 3600 * 10 + 1800
    }
];

// Category labels in Arabic
const categoryLabels = {
    all: 'الكل',
    electronics: 'إلكترونيات',
    fashion: 'أزياء',
    home: 'المنزل',
    beauty: 'جمال',
    gadgets: 'أجهزة'
};

// State
let currentCategory = 'all';
let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
let serverProducts = [];
let allProducts = [...products, ...serverProducts];

// DOM Elements
const productsGrid = document.getElementById('productsGrid');
const dealsSlider = document.getElementById('dealsSlider');
const dealsPrev = document.getElementById('dealsPrev');
const dealsNext = document.getElementById('dealsNext');
const dealsDots = document.getElementById('dealsDots');
const searchInput = document.getElementById('searchInput');
const searchClear = document.getElementById('searchClear');
const searchBtn = document.getElementById('searchBtn');
const categoryBtns = document.querySelectorAll('.category-btn');
const modal = document.getElementById('productModal');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenuClose = document.getElementById('mobileMenuClose');
const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
const mobileMenuPanel = document.getElementById('mobileMenuPanel');
const mobileSearchBtn = document.getElementById('mobileSearchBtn');
const mobileSearch = document.getElementById('mobileSearch');
const mobileSearchInput = document.getElementById('mobileSearchInput');
const mobileSearchSubmit = document.getElementById('mobileSearchSubmit');
const mobileSearchClose = document.getElementById('mobileSearchClose');
const backToTop = document.getElementById('backToTop');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    initCountdown();
    
    initEventListeners();
    try { await fetchProducts(); } catch(e) {}
    try { renderDeals(deals); } catch(e) {}
    startDealTimers();
    initHeroSlideshow();
    initHeroCoupons();
});

// Fetch products from API
async function fetchProducts() {
    try {
        const res = await fetch('/api/products');
        serverProducts = await res.json();
    } catch (e) {
        serverProducts = [];
    }
    allProducts = [...products, ...serverProducts];
    renderProducts(allProducts);
}

// Hero Slideshow
function initHeroSlideshow() {
    const slideshow = document.getElementById('heroSlideshow');
    const heroImages = [
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1200",
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1200",
        "https://images.unsplash.com/photo-1546868871-af0de0ae72be?w=1200",
        "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=1200",
        "https://images.unsplash.com/photo-1585298723682-7115561c51b7?w=1200",
        "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=1200"
    ];
    
    heroImages.forEach((img, i) => {
        const slide = document.createElement('div');
        slide.className = 'slide' + (i === 0 ? ' active' : '');
        slide.style.backgroundImage = `url(${img})`;
        slideshow.appendChild(slide);
    });

    let currentHeroSlide = 0;
    const slides = slideshow.querySelectorAll('.slide');

    setInterval(() => {
        slides[currentHeroSlide].classList.remove('active');
        currentHeroSlide = (currentHeroSlide + 1) % slides.length;
        slides[currentHeroSlide].classList.add('active');
    }, 3000);
}

function initHeroCoupons() {
    const track = document.getElementById('heroCouponsTrack');
    if (!track) return;
    const pills = track.innerHTML;
    track.innerHTML = pills + pills;
}

function initCountdown() {
    const target = new Date('2026-07-13T00:00:00').getTime();
    const dEl = document.getElementById('cdDays');
    const hEl = document.getElementById('cdHours');
    const mEl = document.getElementById('cdMinutes');
    const sEl = document.getElementById('cdSeconds');
    if (!dEl) return;

    function tick() {
        const now = Date.now();
        let diff = Math.max(0, target - now);
        const d = Math.floor(diff / 86400000); diff %= 86400000;
        const h = Math.floor(diff / 3600000); diff %= 3600000;
        const m = Math.floor(diff / 60000); diff %= 60000;
        const s = Math.floor(diff / 1000);
        dEl.textContent = String(d).padStart(2, '0');
        hEl.textContent = String(h).padStart(2, '0');
        mEl.textContent = String(m).padStart(2, '0');
        sEl.textContent = String(s).padStart(2, '0');
    }
    tick();
    setInterval(tick, 1000);
}

// Render Products
function renderProducts(productsToRender) {
    productsGrid.innerHTML = productsToRender.map(product => `
        <div class="product-card" data-id="${product.id}">
            <div class="product-image">
                <img src="${product.image}" alt="${product.title}" loading="lazy">
                <span class="product-badge">${product.badge}</span>
            </div>
            <div class="product-info">
                <span class="product-category">${categoryLabels[product.category] || product.category}</span>
                <h3 class="product-title">${product.shortTitle || product.title}</h3>
                <div class="product-rating">
                    ${renderStars(product.rating)}
                    <span>(${product.reviews})</span>
                </div>
                <div class="product-price">
                    <span class="current-price">$${product.price.toFixed(2)}</span>
                    <span class="current-price-dzd">${Math.round(product.price * USD_TO_DZD)} دج</span>
                    <span class="original-price">$${product.originalPrice.toFixed(2)}</span>
                    <span class="discount">-${Math.round((1 - product.price / product.originalPrice) * 100)}%</span>
                </div>
                <button class="product-btn product-btn-buy" onclick="openCouponModal(${product.id})">
                    <i class="fas fa-shopping-cart"></i> شراء الآن
                </button>
            </div>
        </div>
    `).join('');
}

// Render Deals
function renderDeals(dealsToRender) {
    dealsSlider.innerHTML = dealsToRender.map(deal => `
        <div class="deal-card">
            <span class="deal-badge">${deal.badge}</span>
            <img src="${deal.image}" alt="${deal.title}">
            <div class="deal-info">
                <h3>${deal.title}</h3>
                <p class="product-price" style="margin: 15px 0;">
                    <span class="current-price">$${deal.price.toFixed(2)}</span>
                    <span class="current-price-dzd">${Math.round(deal.price * USD_TO_DZD)} دج</span>
                    <span class="original-price">$${deal.originalPrice.toFixed(2)}</span>
                </p>
                <div class="deal-timer" data-ends="${deal.endsIn}">
                    <div class="timer-box"><span class="days">00</span><small>أيام</small></div>
                    <div class="timer-box"><span class="hours">00</span><small>ساعات</small></div>
                    <div class="timer-box"><span class="minutes">00</span><small>دقائق</small></div>
                    <div class="timer-box"><span class="seconds">00</span><small>ثواني</small></div>
                </div>
            </div>
        </div>
    `).join('');
}

// Render Stars
function renderStars(rating) {
    const r = parseFloat(rating) || 0;
    const fullStars = Math.floor(r);
    const hasHalfStar = r % 1 >= 0.5;
    let stars = '';
    
    for (let i = 0; i < fullStars; i++) {
        stars += '<i class="fas fa-star"></i>';
    }
    if (hasHalfStar) {
        stars += '<i class="fas fa-star-half-alt"></i>';
    }
    const remaining = 5 - fullStars - (hasHalfStar ? 1 : 0);
    for (let i = 0; i < remaining; i++) {
        stars += '<i class="far fa-star"></i>';
    }
    return stars;
}

// Event Listeners
function initEventListeners() {
    // Category filter
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            categoryBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.category;
            filterProducts();
            document.getElementById('products').scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    // Search
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            if (searchClear) searchClear.style.display = searchInput.value ? 'flex' : 'none';
            filterProducts();
        });
        searchInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') {
                const wrapper = document.querySelector('.search-input-wrapper');
                if (wrapper) { wrapper.classList.remove('searching'); void wrapper.offsetWidth; wrapper.classList.add('searching'); }
            }
        });
        searchInput.addEventListener('focus', () => {
            if (searchClear) searchClear.style.display = searchInput.value ? 'flex' : 'none';
        });
    }
    if (searchClear) searchClear.addEventListener('click', () => {
        searchInput.value = '';
        searchClear.style.display = 'none';
        filterProducts();
        searchInput.focus();
    });

    // Modal close
    const modalCloseBtn = document.getElementById('modalClose');
    if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
    if (modal) modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // Wishlist
    productsGrid.addEventListener('click', (e) => {
        const wishlistBtn = e.target.closest('.product-wishlist');
        if (wishlistBtn) {
            e.stopPropagation();
            toggleWishlist(parseInt(wishlistBtn.dataset.id));
            wishlistBtn.classList.toggle('active');
        }
    });

    // Back to top + header hide on scroll
    let lastScroll = 0;
    const header = document.querySelector('.header');
    const categoriesBar = document.querySelector('.categories-bar');
    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;
        if (currentScroll > lastScroll && currentScroll > 100) {
            header.classList.add('header-hidden');
            if (categoriesBar) categoriesBar.classList.add('bar-top');
        } else {
            header.classList.remove('header-hidden');
            if (categoriesBar) categoriesBar.classList.remove('bar-top');
        }
        lastScroll = currentScroll;
        backToTop.classList.toggle('visible', currentScroll > 500);
    });

    // Dark mode toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark');
            const isDark = document.body.classList.contains('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
    }

    // Mobile menu
    if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', openMobileMenu);
    if (mobileMenuClose) mobileMenuClose.addEventListener('click', closeMobileMenu);
    if (mobileMenuOverlay) mobileMenuOverlay.addEventListener('click', closeMobileMenu);

    // Mobile menu links - close menu on click
    document.querySelectorAll('.mobile-menu-link').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // Mobile search
    if (mobileSearchBtn) mobileSearchBtn.addEventListener('click', toggleMobileSearch);
    if (mobileSearchClose) mobileSearchClose.addEventListener('click', closeMobileSearch);
    if (mobileSearchSubmit) mobileSearchSubmit.addEventListener('click', () => {
        if (searchInput) searchInput.value = mobileSearchInput.value;
        filterProducts();
        closeMobileSearch();
    });
    if (mobileSearchInput) mobileSearchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            if (searchInput) searchInput.value = mobileSearchInput.value;
            filterProducts();
            closeMobileSearch();
        }
    });

    // Deals carousel
    initDealsCarousel();
}

// Mobile Menu
function openMobileMenu() {
    mobileMenuPanel.classList.add('active');
    mobileMenuOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeMobileMenu() {
    mobileMenuPanel.classList.remove('active');
    mobileMenuOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Mobile Search
function toggleMobileSearch() {
    mobileSearch.classList.toggle('active');
    if (mobileSearch.classList.contains('active')) {
        mobileSearchInput.focus();
    }
}

function closeMobileSearch() {
    mobileSearch.classList.remove('active');
    mobileSearchInput.value = '';
}

// Deals Carousel
let currentSlide = 0;
let slidesPerView = 3;
let totalSlides = 0;
let autoSlideInterval;

function initDealsCarousel() {
    updateSlidesPerView();
    totalSlides = deals.length;
    renderDots();
    updateCarousel();

    dealsPrev.addEventListener('click', () => {
        currentSlide = Math.max(0, currentSlide - 1);
        updateCarousel();
        resetAutoSlide();
    });

    dealsNext.addEventListener('click', () => {
        const maxSlide = Math.max(0, totalSlides - slidesPerView);
        currentSlide = Math.min(maxSlide, currentSlide + 1);
        updateCarousel();
        resetAutoSlide();
    });

    window.addEventListener('resize', () => {
        updateSlidesPerView();
        const maxSlide = Math.max(0, totalSlides - slidesPerView);
        if (currentSlide > maxSlide) currentSlide = maxSlide;
        renderDots();
        updateCarousel();
    });

    startAutoSlide();
}

function updateSlidesPerView() {
    if (window.innerWidth <= 480) {
        slidesPerView = 1;
    } else if (window.innerWidth <= 768) {
        slidesPerView = 2;
    } else {
        slidesPerView = 3;
    }
}

function updateCarousel() {
    const cardWidth = dealsSlider.querySelector('.deal-card')?.offsetWidth || 300;
    const gap = 20;
    const offset = currentSlide * (cardWidth + gap);
    dealsSlider.style.transform = `translateX(${offset}px)`;

    document.querySelectorAll('.deals-dots .dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === currentSlide);
    });
}

function renderDots() {
    const dotCount = Math.max(1, totalSlides - slidesPerView + 1);
    dealsDots.innerHTML = '';
    for (let i = 0; i < dotCount; i++) {
        const dot = document.createElement('button');
        dot.className = 'dot' + (i === currentSlide ? ' active' : '');
        dot.addEventListener('click', () => {
            currentSlide = i;
            updateCarousel();
            resetAutoSlide();
        });
        dealsDots.appendChild(dot);
    }
}

function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
        const maxSlide = Math.max(0, totalSlides - slidesPerView);
        currentSlide = currentSlide >= maxSlide ? 0 : currentSlide + 1;
        updateCarousel();
    }, 4000);
}

function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
}

// Dark Mode Toggle
// Filter Products
function filterProducts() {
    const searchTerm = searchInput.value.toLowerCase();
    let filtered = allProducts;
    
    if (currentCategory !== 'all') {
        filtered = filtered.filter(p => p.category === currentCategory);
    }
    
    if (searchTerm) {
        filtered = filtered.filter(p => 
            p.title.toLowerCase().includes(searchTerm) ||
            p.category.toLowerCase().includes(searchTerm) ||
            p.description.toLowerCase().includes(searchTerm)
        );
    }
    
    renderProducts(filtered);
}

// Modal Functions
function openProductModal(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;
    
    document.getElementById('modalImage').src = product.image;
    document.getElementById('modalTitle').textContent = product.title;
    document.getElementById('modalRating').innerHTML = `
        ${renderStars(product.rating)}
        <span>${product.rating} (${product.reviews} تقييم)</span>
    `;
    document.getElementById('modalPrice').innerHTML = `
        $${product.price.toFixed(2)}
        <span class="modal-price-dzd">${Math.round(product.price * USD_TO_DZD)} دج</span>
        <span style="text-decoration: line-through; color: var(--text-muted); font-size: 1rem; margin-left: 10px;">$${product.originalPrice.toFixed(2)}</span>
        <span style="background: rgba(255, 71, 87, 0.1); color: #ff4757; padding: 3px 8px; border-radius: 5px; font-size: 0.9rem; margin-left: 10px;">
            وفّر ${Math.round((1 - product.price / product.originalPrice) * 100)}%
        </span>
    `;
    document.getElementById('modalDescription').textContent = product.description;
    document.getElementById('modalLink').href = toAffiliateLink(product.affiliateLink);
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Coupon Modal
const couponModal = document.getElementById('couponModal');
const couponCodeText = document.getElementById('couponCodeText');
const couponCopyBtn = document.getElementById('couponCopyBtn');
const couponGoBtn = document.getElementById('couponGoBtn');
const couponNoCode = document.getElementById('couponNoCode');

function openCouponModal(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;

    if (product.coupon) {
        couponCodeText.textContent = product.coupon;
        couponCodeText.style.display = 'inline';
        couponCopyBtn.style.display = 'flex';
        couponNoCode.style.display = 'none';
    } else {
        couponCodeText.style.display = 'none';
        couponCopyBtn.style.display = 'none';
        couponNoCode.style.display = 'block';
    }

    couponGoBtn.href = toAffiliateLink(product.affiliateLink);
    couponCopyBtn.classList.remove('copied');
    couponCopyBtn.innerHTML = '<i class="fas fa-copy"></i> نسخ';

    couponModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeCouponModal() {
    couponModal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

couponModal.addEventListener('click', (e) => {
    if (e.target === couponModal) closeCouponModal();
});

document.getElementById('couponModalClose').addEventListener('click', closeCouponModal);

couponCopyBtn.addEventListener('click', () => {
    const code = couponCodeText.textContent;
    navigator.clipboard.writeText(code).then(() => {
        couponCopyBtn.classList.add('copied');
        couponCopyBtn.innerHTML = '<i class="fas fa-check"></i> تم النسخ';
        setTimeout(() => {
            couponCopyBtn.classList.remove('copied');
            couponCopyBtn.innerHTML = '<i class="fas fa-copy"></i> نسخ';
        }, 2000);
    });
});

// Wishlist
function toggleWishlist(productId) {
    if (wishlist.includes(productId)) {
        wishlist = wishlist.filter(id => id !== productId);
    } else {
        wishlist.push(productId);
    }
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
}

// Deal Timers
function startDealTimers() {
    const timerElements = document.querySelectorAll('.deal-timer');
    
    timerElements.forEach(timer => {
        let endsIn = parseInt(timer.dataset.ends);
        
        const updateTimer = () => {
            if (endsIn <= 0) return;
            endsIn--;
            timer.dataset.ends = endsIn;
            
            const days = Math.floor(endsIn / 86400);
            const hours = Math.floor((endsIn % 86400) / 3600);
            const minutes = Math.floor((endsIn % 3600) / 60);
            const seconds = endsIn % 60;
            
            timer.querySelector('.days').textContent = String(days).padStart(2, '0');
            timer.querySelector('.hours').textContent = String(hours).padStart(2, '0');
            timer.querySelector('.minutes').textContent = String(minutes).padStart(2, '0');
            timer.querySelector('.seconds').textContent = String(seconds).padStart(2, '0');
        };
        
        updateTimer();
        setInterval(updateTimer, 1000);
    });
}

// Escape key closes modal, mobile menu, and search
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
        closeCouponModal();
        closeMobileMenu();
        closeMobileSearch();
    }
});

function copyCoupon(el) {
    const code = el.textContent;
    navigator.clipboard.writeText(code).then(() => {
        el.classList.add('copied');
        const original = el.innerHTML;
        el.innerHTML = '<i class="fas fa-check"></i>';
        setTimeout(() => {
            el.classList.remove('copied');
            el.innerHTML = original;
        }, 1500);
    });
}

function copyCouponCode(el, code) {
    navigator.clipboard.writeText(code).then(() => {
        el.classList.add('copied');
        const flash = document.createElement('span');
        flash.className = 'copied-flash';
        el.appendChild(flash);
        const icon = el.querySelector('.hcp-icon');
        if (icon) icon.innerHTML = '<i class="fas fa-check"></i>';
        setTimeout(() => {
            el.classList.remove('copied');
            if (flash.parentNode) flash.remove();
            if (icon) icon.innerHTML = '<i class="fas fa-copy"></i>';
        }, 1500);
    });
}

// Auto-scroll coupon slider
const couponsScroll = document.querySelector('.coupons-scroll');

function scrollCoupons(dir) {
    if (!couponsScroll) return;
    const scrollAmount = 250;
    couponsScroll.scrollBy({ left: dir === 'right' ? -scrollAmount : scrollAmount, behavior: 'smooth' });
}

if (couponsScroll) {
    let scrollDir = 1;
    let scrollPaused = false;

    couponsScroll.addEventListener('mouseenter', () => scrollPaused = true);
    couponsScroll.addEventListener('mouseleave', () => scrollPaused = false);
    couponsScroll.addEventListener('touchstart', () => scrollPaused = true);
    couponsScroll.addEventListener('touchend', () => {
        setTimeout(() => scrollPaused = false, 2000);
    });

    setInterval(() => {
        if (scrollPaused) return;
        if (couponsScroll.scrollLeft + couponsScroll.clientWidth >= couponsScroll.scrollWidth) {
            scrollDir = -1;
        } else if (couponsScroll.scrollLeft <= 0) {
            scrollDir = 1;
        }
        couponsScroll.scrollLeft += scrollDir;
    }, 30);
}
