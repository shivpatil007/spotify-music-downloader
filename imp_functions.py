
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
