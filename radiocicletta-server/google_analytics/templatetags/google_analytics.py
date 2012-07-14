from django.conf import settings
from django.template import Library

GOOGLE_ANALYTICS_ID = getattr(settings, 'GOOGLE_ANALYTICS_ID', None)
GOOGLE_ANALYTICS_DOMAIN = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', None)

register = Library()

@register.inclusion_tag('google_analytics/code.html')
def google_analytics_code(analytics_id=GOOGLE_ANALYTICS_ID, analytics_domain=GOOGLE_ANALYTICS_DOMAIN):
    return {'google_analytics_id': analytics_id, 'google_analytics_domain': analytics_domain}
