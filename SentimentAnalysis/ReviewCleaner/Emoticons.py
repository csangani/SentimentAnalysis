prefix = 'EMOTICON'

emoticonMap = {
       ':)':    'smile',
       ':-)':   'smile',
       ':]':    'smile',
       ':-]':   'smile',
       '(:':    'smile',
       '(-:':   'smile',
       ';)':    'wink',
       ';-)':   'wink',
       ':P':    'cheeky',
       ':-P':   'cheeky',
       ';P':    'cheeky',
       ';-P':   'cheeky',
       ';D':    'laugh',
       ';-D':   'laugh',
       ':D':    'laugh',
       ':-D':   'laugh',
       ':(':    'sad',
       ':-(':   'sad',
       ';(':    'sad',
       ';-(':   'sad',
       '):':    'sad',
       ')-:':   'sad',
       ':[':    'sad',
       ':-[':   'sad',
       ':/':    'wry',
       ':-/':   'wry',
       ';/':    'wry',
       ';-/':   'wry',
       ':\\':   'wry',
       ':-\\':  'wry',
       ';\\':   'wry',
       ';-\\':  'wry',
       ':\'(':  'cry',
       ':\'-(': 'cry',
       '<3':    'love',
       '>:(':   'angry',
       '>:-(':  'angry',
       '>;(':   'angry',
       '>;-(':  'angry',
       'O.O':   'bigeyes',
       'o.O':   'bigeyes',
       'O.o':   'bigeyes',
       '-.-':   'squint'
       }

def replace(str):
    for e in emoticonMap:
        str = str.replace(e, prefix + emoticonMap[e])
    return str