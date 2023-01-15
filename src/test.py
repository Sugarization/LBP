from support import *
from subprocess import run
setSystemPath()

print(getPlatform())
print(getPrompt())

run('blastn')