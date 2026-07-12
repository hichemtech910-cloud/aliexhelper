// DZ Express - API Configuration
// أضف مفاتيح AliExpress Affiliate API هنا
// سجل في: https://portals.aliexpress.com

const API_CONFIG = {
    appKey: '502678',
    appSecret: '79wEXy290DEyur5A7wcpsQ2H8OmwmuFz',
    trackingId: 'hixem'
};

// دالة تحويل الرابط العادي إلى رابط إحالة
function toAffiliateLink(url) {
    if (!url || !url.includes('aliexpress.com')) return url;
    // إذا كان الرابط يحتوي على click.aliexpress فهو رابط إحالة بالفعل
    if (url.includes('s.click.aliexpress.com') || url.includes('aff_platform')) return url;
    // الرابط العادي — نعيده كما هو لأنه لا يمكن التحويل بدون API
    return url;
}
