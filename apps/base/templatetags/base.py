from django import template

import re

register = template.Library()

@register.assignment_tag(takes_context=True)
def is_mobile(context):
    if 'HTTP_USER_AGENT' not in context['request'].META:
        return False
    return re.search('(android|blackberry|iphone|palm|windows (ce|phone))',
                     context['request'].META['HTTP_USER_AGENT'], re.IGNORECASE)

@register.assignment_tag(takes_context=True)
def gather_analytics(context):
    if 'SERVER_NAME' not in context['request'].META:
        return False
    return context['request'].META['SERVER_NAME'] == 'andreinicholson.com'
