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
    // s.click links are already affiliate links from the API
    if (url.includes('s.click.aliexpress.com')) return url;
    // aff_id links are already affiliate links
    if (url.includes('aff_id=')) return url;
    // aff_platform links are already affiliate links
    if (url.includes('aff_platform')) return url;
    // Regular link - add aff_id
    const separator = url.includes('?') ? '&' : '?';
    return url + separator + 'aff_id=hixem';
}
