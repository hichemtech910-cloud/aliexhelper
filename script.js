// Sample Products Data - Replace with your AliExpress affiliate links
const products = [
    {
        id: 1,
        title: "سماعات بلوتوث لاسلكية برو",
        category: "electronics",
        price: 12.99,
        originalPrice: 29.99,
        rating: 4.8,
        reviews: 2541,
        image: "https://images.unsplash.com/photo-1590658268037-6bf12f032f55?w=400",
        badge: "الأكثر مبيعاً",
        description: "سماعات لاسلكية عالية الجودة مع خاصية إلغاء الضوضاء وعمر بطارية 24 ساعة. مثالية لعشاق الموسيقى والمهنيين.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 2,
        title: "ساعة ذكية متعددة الوظائف",
        category: "gadgets",
        price: 24.99,
        originalPrice: 49.99,
        rating: 4.7,
        reviews: 1893,
        image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
        badge: "-50%",
        description: "ساعة ذكية متكاملة الميزات مع مراقبة ضربات القلب وGPS وعمر بطارية 7 أيام.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 3,
        title: "سماعة بلوتوث محمولة",
        category: "electronics",
        price: 18.50,
        originalPrice: 35.00,
        rating: 4.6,
        reviews: 3210,
        image: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
        badge: "رائجة",
        description: "سماعة محمولة مقاومة للماء مع صوت 360 درجة ووقت تشغيل 12 ساعة.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 4,
        title: "إضاءة LED حلقة مع حامل",
        category: "home",
        price: 15.99,
        originalPrice: 32.00,
        rating: 4.9,
        reviews: 4521,
        image: "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=400",
        badge: "الأعلى تقييماً",
        description: "إضاءة LED احترافية بقطر 10 بوصات مثالية للبث المباشر والتصوير ومكياج.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 5,
        title: "مجموعة أوشحة حريرية أنيقة",
        category: "fashion",
        price: 8.99,
        originalPrice: 19.99,
        rating: 4.5,
        reviews: 892,
        image: "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400",
        badge: "جديد",
        description: "أوشحة حريرية أنيقة بتصاميم جميلة. إكسسوارات مثالية لأي إطلالة.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 6,
        title: "مجموعة العناية بالبشرة فاخرة",
        category: "beauty",
        price: 19.99,
        originalPrice: 45.00,
        rating: 4.8,
        reviews: 1567,
        image: "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400",
        badge: "شائعة",
        description: "روتين عناية بالبشرة كامل يشمل التونر والسيروم والمرطب.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 7,
        title: "محول USB-C متعدد المنافذ",
        category: "gadgets",
        price: 22.99,
        originalPrice: 42.00,
        rating: 4.7,
        reviews: 2134,
        image: "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400",
        badge: "أساسي",
        description: "محول USB-C بـ 7 منافذ مع HDMI ومنافذ USB 3.0 وقارئ بطاقات SD.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 8,
        title: "مجموعة أصص نباتات سيراميك",
        category: "home",
        price: 14.99,
        originalPrice: 28.00,
        rating: 4.6,
        reviews: 987,
        image: "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400",
        badge: "صديق للبيئة",
        description: "مجموعة من 3 أصص سيراميك عصرية مع ثقوب تصريف. مثالية للنباتات المنزلية.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 9,
        title: "حذاء رياضي بسيط وأنيق",
        category: "fashion",
        price: 16.99,
        originalPrice: 34.99,
        rating: 4.5,
        reviews: 3456,
        image: "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400",
        badge: "رائج",
        description: "حذاء رياضي مريح مع نعل مبطن بال-memory foam. متوفر بعدة ألوان.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 10,
        title: "جهاز عرض فيديو مصغر HD",
        category: "electronics",
        price: 39.99,
        originalPrice: 79.99,
        rating: 4.4,
        reviews: 1234,
        image: "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400",
        badge: "-50%",
        description: "جهاز عرض فيديو محمول بدقة 1080p. مثالي لمشاهدة الأفلام والعرض التقديمي.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 11,
        title: "مجموعة أدوات تصفيف الشعر",
        category: "beauty",
        price: 28.99,
        originalPrice: 55.00,
        rating: 4.7,
        reviews: 876,
        image: "https://images.unsplash.com/photo-1522338242992-e1a54571a7c8?w=400",
        badge: "مجموعة كاملة",
        description: "أدوات تصفيف الشعر الاحترافية تشمل مكواة الفرد والتجعيد والمجفف.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    },
    {
        id: 12,
        title: "شاحن لاسلكي سريع",
        category: "gadgets",
        price: 9.99,
        originalPrice: 19.99,
        rating: 4.6,
        reviews: 2890,
        image: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400",
        badge: "شحن سريع",
        description: "شاحن لاسلكي 15 واط سريع متوافق مع جميع الأجهزة المدعومة بـ Qi.",
        affiliateLink: "https://aliexpress.com/item/YOUR_PRODUCT_ID.html?aff_platform=YOUR_AFFILIATE_ID"
    }
];

const deals = [
    {
        id: 101,
        title: "عرض محدود - مجموعة المنزل الذكي",
        image: "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=400",
        badge: "خصم 60%",
        price: 49.99,
        originalPrice: 129.99,
        endsIn: 86400 * 2 + 3600 * 5
    },
    {
        id: 102,
        title: "مجموعة الصيف - عروض الأزياء",
        image: "https://images.unsplash.com/photo-1445205170230-053b83016050?w=400",
        badge: "خصم 45%",
        price: 29.99,
        originalPrice: 54.99,
        endsIn: 86400 + 3600 * 12
    },
    {
        id: 103,
        title: "تخفيضات كبيرة على الأجهزة التقنية",
        image: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=400",
        badge: "خصم 70%",
        price: 19.99,
        originalPrice: 66.99,
        endsIn: 3600 * 8 + 1800
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
let isDarkMode = localStorage.getItem('darkMode') === 'true';

// DOM Elements
const productsGrid = document.getElementById('productsGrid');
const dealsSlider = document.getElementById('dealsSlider');
const searchInput = document.getElementById('searchInput');
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
const darkModeBtn = document.getElementById('darkModeBtn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Apply saved dark mode
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        darkModeBtn.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    renderProducts(products);
    renderDeals(deals);
    initEventListeners();
    startDealTimers();
});

// Render Products
function renderProducts(productsToRender) {
    productsGrid.innerHTML = productsToRender.map(product => `
        <div class="product-card" data-id="${product.id}">
            <div class="product-image">
                <img src="${product.image}" alt="${product.title}" loading="lazy">
                <span class="product-badge">${product.badge}</span>
                <button class="product-wishlist ${wishlist.includes(product.id) ? 'active' : ''}" data-id="${product.id}">
                    <i class="fas fa-heart"></i>
                </button>
            </div>
            <div class="product-info">
                <span class="product-category">${categoryLabels[product.category] || product.category}</span>
                <h3 class="product-title">${product.title}</h3>
                <div class="product-rating">
                    ${renderStars(product.rating)}
                    <span>(${product.reviews})</span>
                </div>
                <div class="product-price">
                    <span class="current-price">$${product.price.toFixed(2)}</span>
                    <span class="original-price">$${product.originalPrice.toFixed(2)}</span>
                    <span class="discount">-${Math.round((1 - product.price / product.originalPrice) * 100)}%</span>
                </div>
                <button class="product-btn" onclick="openProductModal(${product.id})">
                    <i class="fas fa-eye"></i> عرض سريع
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
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
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
        });
    });

    // Search
    searchBtn.addEventListener('click', filterProducts);
    searchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') filterProducts();
    });

    // Modal close
    document.getElementById('modalClose').addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
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

    // Back to top
    window.addEventListener('scroll', () => {
        backToTop.classList.toggle('visible', window.scrollY > 500);
    });

    // Newsletter form
    document.getElementById('newsletterForm').addEventListener('submit', (e) => {
        e.preventDefault();
        alert('شكراً لاشتراكك! تحقق من بريدك الإلكتروني للحصول على العروض الحصرية.');
        e.target.reset();
    });

    // Mobile menu
    mobileMenuBtn.addEventListener('click', openMobileMenu);
    mobileMenuClose.addEventListener('click', closeMobileMenu);
    mobileMenuOverlay.addEventListener('click', closeMobileMenu);

    // Mobile menu links - close menu on click
    document.querySelectorAll('.mobile-menu-link').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // Mobile search
    mobileSearchBtn.addEventListener('click', toggleMobileSearch);
    mobileSearchClose.addEventListener('click', closeMobileSearch);
    mobileSearchSubmit.addEventListener('click', () => {
        searchInput.value = mobileSearchInput.value;
        filterProducts();
        closeMobileSearch();
    });
    mobileSearchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            searchInput.value = mobileSearchInput.value;
            filterProducts();
            closeMobileSearch();
        }
    });

    // Dark mode toggle
    darkModeBtn.addEventListener('click', toggleDarkMode);

    // Touch swipe for deals slider
    initDealsSwipe();
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

// Deals touch swipe
function initDealsSwipe() {
    let startX = 0;
    let scrollLeft = 0;
    let isDown = false;

    dealsSlider.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - dealsSlider.offsetLeft;
        scrollLeft = dealsSlider.scrollLeft;
        dealsSlider.style.cursor = 'grabbing';
    });

    dealsSlider.addEventListener('mouseleave', () => {
        isDown = false;
        dealsSlider.style.cursor = 'grab';
    });

    dealsSlider.addEventListener('mouseup', () => {
        isDown = false;
        dealsSlider.style.cursor = 'grab';
    });

    dealsSlider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - dealsSlider.offsetLeft;
        const walk = (x - startX) * 1.5;
        dealsSlider.scrollLeft = scrollLeft - walk;
    });

    // Touch events
    dealsSlider.addEventListener('touchstart', (e) => {
        isDown = true;
        startX = e.touches[0].pageX - dealsSlider.offsetLeft;
        scrollLeft = dealsSlider.scrollLeft;
    });

    dealsSlider.addEventListener('touchend', () => {
        isDown = false;
    });

    dealsSlider.addEventListener('touchmove', (e) => {
        if (!isDown) return;
        const x = e.touches[0].pageX - dealsSlider.offsetLeft;
        const walk = (x - startX) * 1.5;
        dealsSlider.scrollLeft = scrollLeft - walk;
    });

    dealsSlider.style.cursor = 'grab';
}

// Dark Mode Toggle
function toggleDarkMode() {
    isDarkMode = !isDarkMode;
    document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
    darkModeBtn.innerHTML = isDarkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    localStorage.setItem('darkMode', isDarkMode);
}

// Filter Products
function filterProducts() {
    const searchTerm = searchInput.value.toLowerCase();
    let filtered = products;
    
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
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    document.getElementById('modalImage').src = product.image;
    document.getElementById('modalTitle').textContent = product.title;
    document.getElementById('modalRating').innerHTML = `
        ${renderStars(product.rating)}
        <span>${product.rating} (${product.reviews} تقييم)</span>
    `;
    document.getElementById('modalPrice').innerHTML = `
        $${product.price.toFixed(2)}
        <span style="text-decoration: line-through; color: var(--text-muted); font-size: 1rem; margin-left: 10px;">$${product.originalPrice.toFixed(2)}</span>
        <span style="background: rgba(255, 71, 87, 0.1); color: #ff4757; padding: 3px 8px; border-radius: 5px; font-size: 0.9rem; margin-left: 10px;">
            وفّر ${Math.round((1 - product.price / product.originalPrice) * 100)}%
        </span>
    `;
    document.getElementById('modalDescription').textContent = product.description;
    document.getElementById('modalLink').href = product.affiliateLink;
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

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
        closeMobileMenu();
        closeMobileSearch();
    }
});
