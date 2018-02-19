import i18n
import os

i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'json')

i18n.load_path.append("adventurelib/res/locale")

def t(key, **kwargs):
    return i18n.t(key, **kwargs)


