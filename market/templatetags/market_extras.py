from django import template

register = template.Library()

@register.inclusion_tag('market/_seller_card.html')
def show_seller_card(user):
    return {'seller': user}