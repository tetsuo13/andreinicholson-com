from django_assets import Bundle, register

register('css_all', Bundle('css/base.css',
                           filters='cssutils', output='content.css'))
