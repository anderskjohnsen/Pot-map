"""Parse dwrolvink/titanmap save_file.js into structured location objects."""
import re, json
from collections import Counter

raw = open('/tmp/save_file.js').read()
blocks = raw.split('obj = newRect(ObjectList.objects);')

def grab(b, prop):
    m = re.search(r'obj\.' + re.escape(prop) + r'\s*=\s*(.+?);', b)
    return m.group(1).strip() if m else None

def num(b, prop):
    v = grab(b, prop)
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

objs = []
for b in blocks[1:]:
    text = grab(b, 'text')
    if text:
        text = text.strip('"\'')
    icon = grab(b, 'bg_image_id')
    if icon:
        icon = icon.strip('"\'')
    objs.append(dict(
        x=num(b, 'pos.x'), y=num(b, 'pos.y'),
        text=text or '', icon=icon or '', w=num(b, 'width'),
    ))

out = []
out.append(f'parsed objects: {len(objs)}')
out.append('\nICON counts:')
for k, c in Counter(o['icon'] for o in objs).most_common():
    out.append(f'  {c:>4}  {k!r}')
named = [o for o in objs if o['text']]
out.append(f'\nnamed objects: {len(named)}')
xs = [o['x'] for o in objs if o['x'] is not None]
ys = [o['y'] for o in objs if o['y'] is not None]
out.append(f'x range: {min(xs):.1f} .. {max(xs):.1f}')
out.append(f'y range: {min(ys):.1f} .. {max(ys):.1f}')
out.append('\nsample named objects:')
for o in named[:40]:
    out.append(f"  icon={o['icon']:<14} ({o['x']},{o['y']})  {o['text'][:40]}")

json.dump(objs, open('/tmp/objs.json', 'w'))
open('/tmp/parse_out.txt', 'w').write('\n'.join(out))
print('OK wrote /tmp/parse_out.txt and /tmp/objs.json')
