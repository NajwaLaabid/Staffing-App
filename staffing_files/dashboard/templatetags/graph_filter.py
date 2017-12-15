from django.template.defaulttags import register

@register.filter
def compute_difference(value, arg):
    return value - arg
