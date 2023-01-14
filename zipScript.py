import zipfile

zippedFile = zipfile.ZipFile('code.zip', 'w')

zippedFile.write('actions.py')
zippedFile.write('application.py')
zippedFile.write('bot.py')
zippedFile.write('game_message.py')
zippedFile.close()