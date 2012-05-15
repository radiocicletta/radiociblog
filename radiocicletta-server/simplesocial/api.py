from django.conf import settings
from django.utils.html import escape
from django.utils.http import urlquote
from mediagenerator.utils import media_url

#TODO: commentone twitterone che fa cacare l'iframone.
#WIDE_TWITTER_BUTTON = """
#<iframe src="http://platform.twitter.com/widgets/tweet_button.html?count=horizontal&amp;lang=en&amp;text=%(title)s&amp;url=%(url)s%(opttwitteruser)s" style="width: 135px; height: 20px; border: none; overflow: hidden;"></iframe>
#"""
WIDE_TWITTER_BUTTON = ""
FACEBOOK_LIKE_BUTTON = """
<iframe src="http://www.facebook.com/plugins/like.php?href=%(url)s&amp;layout=button_count&amp;show_faces=false&amp;width=100&amp;height=21&amp;action=like&amp;colorscheme=light" style="width: 100px; height: 21px; border: none; overflow: hidden; align: left; margin: 0px 0px 0px 0px;"></iframe>
"""

PLUS_ONE_BUTTON = """
<div class="g-plusone" data-size="standard" data-count="true" data-href="%(rawurl)s"></div>
"""

WIDE_BUTTONS_DIV = '<div class="wide-share-buttons" style="overflow:hidden; margin-bottom: 8px;">%s</div>'
NARROW_BUTTONS_DIV = '<ul class="narrow-share-buttons">%s</ul>'

BASE_BUTTON = '<li><a class="simplesocial" title="%(title)s" href="%(url)s">%(title)s</a></li>'

DEFAULT_TITLE = 'Condividi su %s'

NARROW_BUTTONS = {
    'Twitter': {
        'title': 'Retweet',
        'url': 'http://twitter.com/share?text=%(title)s&url=%(url)s%(opttwitteruser)s',
    },
    'Facebook': 'http://www.facebook.com/share.php?u=%(url)s&t=%(title)s',
    'Email': {
        'title': 'Invia per email',
        'url': 'http://feedburner.google.com/fb/a/emailFlare?itemTitle=%(title)s&uri=%(url)s',
    },
    'Delicious': 'http://del.icio.us/post?url=%(url)s&title=%(title)s',
    'Digg': 'http://digg.com/submit?url=%(url)s&title=%(title)s',
    'StumbleUpon': 'http://www.stumbleupon.com/submit?url=%(url)s&title=%(title)s',
    'Reddit': 'http://reddit.com/submit?url=%(url)s&title=%(title)s',
    'Technorati': 'http://technorati.com/faves?sub=favthis&add=%(url)s',
}

SHOW_SOCIAL_BUTTONS = getattr(settings, 'SHOW_SOCIAL_BUTTONS',
    ('Twitter', 'Facebook', 'Email', 'Delicious', 'StumbleUpon',
     'Digg', 'Reddit', 'Technorati'))

def narrow_buttons(request, title, url, buttons=SHOW_SOCIAL_BUTTONS):
    base_url = 'http%s://%s' % ('s' if request.is_secure() else '',
                                request.get_host())
    data = _get_url_data(request, title, url)
    code = []
    for name in buttons:
        button = NARROW_BUTTONS[name]
        if not isinstance(button, dict):
            button = {'url': button}
        title = escape(button.get('title', DEFAULT_TITLE % name))
        url = escape(button['url'] % data)
        code.append(BASE_BUTTON % {'title': title, 'url': url})
    return NARROW_BUTTONS_DIV % '\n'.join(code)

def wide_buttons(request, title, url,
                 buttons=(WIDE_TWITTER_BUTTON, PLUS_ONE_BUTTON, FACEBOOK_LIKE_BUTTON)):
    data = _get_url_data(request, title, url)
    data['opttwitteruser'] = escape(data['opttwitteruser'])
    code = [button % data for button in buttons]
    return WIDE_BUTTONS_DIV % '\n'.join(code)

def _get_url_data(request, title, url):
    url = 'http%s://%s%s' % ('s' if request.is_secure() else '',
                             request.get_host(), url)
    data = {'url': url, 'title': title, 'opttwitteruser': ''}
    twitter_username = getattr(settings, 'TWITTER_USERNAME', None)
    if twitter_username:
        data['opttwitteruser'] = twitter_username
    for key in data:
        data[key] = urlquote(data[key])
    if twitter_username:
        data['opttwitteruser'] = '&via=' + data['opttwitteruser']
    data['rawurl'] = url
    return data
