
def random_string(length):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def deleting(id):
    import os
    import glob
    id = str(id)
    try:
        for i in glob.glob('music'+id+'/*'):
            os.remove(i)

        if os.path.exists('music'+id):
            os.rmdir('music'+id)
    except Exception as e:
        print(e)
    try:
        if os.path.exists('playlist'+id+'.zip'):

            os.remove('playlist'+id+'.zip')
    except Exception as e:
        print(e)


def create_directory(id):
    import os
    id = str(id)
    if not os.path.exists('music'+id):
        os.makedirs('music'+id)


def replacesomthing(text):
    a = {
        'å': 'a',
        'ä': 'a',
        'ö': 'o',
        'Ö': 'O',
        'À': 'A',
        'Á': 'A',
        'Â': 'A',
        'Ã': 'A',
        'Ä': 'A',
        'Å': 'A',
        'Æ': 'A',
        ', ': '',
    }

    for i in a:
        text = text.replace(i, a[i])
    return text


def analayse_type_of_link_of_spotify(link):
    import re
    if re.search('playlist', link):
        return 'sp-playlist'
    elif re.search('track', link):
        return 'sp-track'
    elif re.search('album', link):
        return 'sp-album'
    elif re.search('artist', link):
        return 'sp-artist'
    else:
        return 'error'


def analayse_type_of_link_of_youtube(link):
    import re
    if re.search('&list', link):
        return 'yt-playlist'
    elif re.search('watch?v=', link):
        return 'yt-track'
    else:
        return 'error'


def analyse_link_of_spotify_or_youtube(link):
    import re
    if re.search('spotify', link):
        return analayse_type_of_link_of_spotify(link)
    elif re.search('youtube', link) or re.search('youtu.be', link):
        return analayse_type_of_link_of_youtube(link)
    else:
        return 'error'
