from pathlib import Path
from time import time
from uuid import uuid4, uuid5, UUID
from datetime import datetime
KEYPATH = Path(__file__)/'..'/'myKey.key'
with open(KEYPATH, encoding='utf-8')as keyfp:
    KEY = keyfp.read().upper()
mode = input('[B]ase or [A]dvanced?').upper()
valid = int(input('       Valid time(h)?'))*3600
if mode != 'A':
    mode = 'B'
disabled = int(time()+valid)
inited = f'{KEY[:8]}{mode}{disabled:011}'.upper()
inited += str(uuid5(UUID(KEY), inited))[:5].upper()
end = ''
for i in range(5):
    end += inited[i*5:(i+1)*5]
    end += '-'
print(end[:-1])
