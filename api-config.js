// DZ Express - API Configuration
// أضف مفاتيح AliExpress Affiliate API هنا
// سجل في: https://portals.aliexpress.com

const API_CONFIG = {
    appKey: '502678',
    appSecret: 'Ds7f3NQm0EpuK5VUsTVKlS3sRnOkkXoH',
    trackingId: 'hixem'
};

// دالة تحويل الرابط العادي إلى رابط إحالة
function toAffiliateLink(url) {
    if (!url || !url.includes('aliexpress.com')) return url;
    // إذا كان الرابط يحتوي على aff_id فهو رابط إحالة بالفعل
    if (url.includes('aff_id=')) return url;
    // رابط s.click — نحوله لرابط عادي مع aff_id
    if (url.includes('s.click.aliexpress.com')) {
        const match = url.match(/\/item\/(\d+)\.html/);
        if (match) {
            return `https://www.aliexpress.com/item/${match[1]}.html?aff_id=hixem`;
        }
    }
    // رابط عادي — نضيف aff_id
    const separator = url.includes('?') ? '&' : '?';
    return url + separator + 'aff_id=hixem';
}
