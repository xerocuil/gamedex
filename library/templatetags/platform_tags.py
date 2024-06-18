import os
from django import template
from django.template.defaultfilters import stringfilter
import gamedex.settings as settings

register = template.Library()

# @register.filter()
# @stringfilter
# def markdown(value):
    # return md.markdown(value, extensions=['markdown.extensions.fenced_code'])

@register.filter()
@stringfilter
def platform_img(slug, img):
    img_path = os.path.join(
        settings.STATIC_ROOT,
        'shared',
        'platforms',
        slug, img + '.svg')

    if os.path.exists(img_path):
        img_url = settings.STATIC_URL + 'shared/platforms/' + slug + '/' + img + '.svg'
        tag = '<img class="' + img + '" src="' + img_url + '" alt="' + slug + '">'
    else:
        tag = slug

    return tag
