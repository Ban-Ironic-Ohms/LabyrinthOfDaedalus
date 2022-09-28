from contextlib import redirect_stdout
import io, os, subprocess, sys


# sys.path.append("../../")
sys.path.append("/home/micah/Documents/LabyrinthOfDaedalus/")
from main import main
from another import heyo

for i in heyo():
    print(i)

# print(f.getvalue())