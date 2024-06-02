from django import template

register = template.Library()

@register.inclusion_tag('base/stylized_form.html')
def stylize_form(form, button_label):
    return {'form': form, 'button_label': button_label }