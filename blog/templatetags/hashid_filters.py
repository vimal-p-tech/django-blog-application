from django import template
from hashids import Hashids

register = template.Library()
hashids = Hashids(salt="test_id",min_length=8)


@register.filter(name='hashid_encode')
def hashid_encode(pk,title):
    return hashids.encode(pk)
    