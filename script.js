// Sample Products Data - Replace with your AliExpress affiliate links
const USD_TO_DZD = 135;
let products = [];

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
    let scrollTimeout;

    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;
        if (currentScroll > lastScroll && currentScroll > 80) {
            header.classList.add('header-hidden');
            if (categoriesBar) categoriesBar.classList.add('bar-top');
        } else if (currentScroll < lastScroll - 5) {
            header.classList.remove('header-hidden');
            if (categoriesBar) categoriesBar.classList.remove('bar-top');
        }
        lastScroll = currentScroll;
        backToTop.classList.toggle('visible', currentScroll > 400);

        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            if (currentScroll < 80) {
                header.classList.remove('header-hidden');
                if (categoriesBar) categoriesBar.classList.remove('bar-top');
            }
        }, 200);
    }, { passive: true });

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
}

// Mobile Menu
function openMobileMenu() {
    mobileMenuPanel.classList.add('active');
    mobileMenuOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    document.body.style.position = 'fixed';
    document.body.style.width = '100%';
}

function closeMobileMenu() {
    mobileMenuPanel.classList.remove('active');
    mobileMenuOverlay.classList.remove('active');
    document.body.style.overflow = '';
    document.body.style.position = '';
    document.body.style.width = '';
}

// Mobile Search
function toggleMobileSearch() {
    mobileSearch.classList.toggle('active');
    if (mobileSearch.classList.contains('active')) {
        setTimeout(() => mobileSearchInput.focus(), 100);
    }
}

function closeMobileSearch() {
    mobileSearch.classList.remove('active');
    mobileSearchInput.value = '';
}

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
    document.body.style.position = 'fixed';
    document.body.style.width = '100%';
}

function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
    document.body.style.position = '';
    document.body.style.width = '';
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
    document.body.style.position = 'fixed';
    document.body.style.width = '100%';
}

function closeCouponModal() {
    couponModal.classList.remove('active');
    document.body.style.overflow = '';
    document.body.style.position = '';
    document.body.style.width = '';
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
