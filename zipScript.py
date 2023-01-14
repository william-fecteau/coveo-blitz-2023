import zipfile
from os import walk
import pathlib

myPath = pathlib.Path(__file__).parent.resolve()
zippedFile = zipfile.ZipFile('code.zip', 'w')

filenames = next(walk(myPath), (None, None, []))[2]
for i in filenames:
    if i != 'zipScript.py' and i != 'code.zip':
        zippedFile.write(i)

zippedFile.close()