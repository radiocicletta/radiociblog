from django.conf import settings
from django.utils.html import escape
from django.utils.http import urlquote
from mediagenerator.utils import media_url

WIDE_TWITTER_BUTTON = """
<a href="https://twitter.com/share" class="twitter-share-button" data-via="%(opttwitteruser)s" data-lang="it" data-dnt="true">Tweet</a>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
"""

FACEBOOK_LIKE_BUTTON = """
<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/it_IT/all.js#xfbml=1";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>
<div class="fb-like" data-href="%(url)s" data-send="false" data-layout="button_count" data-width="90" data-show-faces="true" data-colorscheme="dark"></div>"""

PLUS_ONE_BUTTON = """
<script type="text/javascript">
  window.___gcfg = {lang: 'it'};
  (function() {
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
    })();
    </script>
<div class="g-plusone" data-size="medium" data-annotation="inline" data-width="80"></div>
"""


LINKEDIN_BUTTON = """
<script src="//platform.linkedin.com/in.js" type="text/javascript"></script>
<script type="IN/Share" data-url="%(url)s" data-counter="right"></script>"""

WIDE_BUTTONS=(WIDE_TWITTER_BUTTON, PLUS_ONE_BUTTON, FACEBOOK_LIKE_BUTTON, LINKEDIN_BUTTON)

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

def wide_buttons(request, title, url):
    data = _get_url_data(request, title, url)
    data['opttwitteruser'] = escape(data['opttwitteruser'])
    code = [button % data for button in WIDE_BUTTONS]
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
    data['rawurl'] = url
    return data
