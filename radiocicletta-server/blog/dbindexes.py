from .models import Blog, Post
from dbindexer.api import register_index
from dbindexer import autodiscover

autodiscover()
register_index(Blog, {'title': 'icontains'})
#register_index(Post, {'title': 'icontains', 'url': 'icontains', 'author':'iexact'})
