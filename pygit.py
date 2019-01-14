import os
import sys

os.system("git add .")
os.system("git commit -am'%s'"%str(sys.argv))
os.system("git push sae 1")

