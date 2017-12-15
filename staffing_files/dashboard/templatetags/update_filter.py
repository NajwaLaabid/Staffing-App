from django.template.defaulttags import register

@register.filter
def indxList(l, idx):
    return l[idx];
