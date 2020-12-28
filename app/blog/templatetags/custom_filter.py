from django import template
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup
from urllib.parse import urlencode

register = template.Library()
printn = lambda x: print('\n\n\n\n', x, '\n\n\n\n')

@register.filter
@stringfilter
def truncatecontent(value, length):
    value = value if isinstance(value, str) else value()
    soup = BeautifulSoup(value, 'html.parser')
    text = soup.p.getText()
    return text[:length] + '...' if text else ''


@register.simple_tag
def edit_query(request, **kwargs):
    query = request.GET.copy()
    query.update(kwargs)
    return urlencode(query)

@register.simple_tag
def new_query(request, *inherit, **kwargs):
    query = request.GET.copy()
    new_query = {i: query[i] for i in query if i in inherit}
    new_query.update(kwargs)
    return urlencode(new_query) 
