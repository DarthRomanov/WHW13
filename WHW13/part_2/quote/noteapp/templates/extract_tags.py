from django import template

register = template.Library()


def author(note_author):
    return ', '.join([str(name) for name in note_author.all()])


register.filter('author', author)
