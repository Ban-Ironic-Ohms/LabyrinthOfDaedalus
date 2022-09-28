from django.shortcuts import render
from django.http import HttpResponse
from contextlib import redirect_stdout
import io, os, subprocess, sys

# sys.path.append("../../")
sys.path.append("/home/micah/Documents/LabyrinthOfDaedalus/")
from main_copy import main
main()

# main()
# a = subprocess.run(["python3", "/home/micah/Documents/LabyrinthOfDaedalus/main.py"], capture_output=True)
# a = subprocess.run(["df", "-h"], capture_output=True)
# print(a.stdout)

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    # with redirect_stdout(io.StringIO()) as f:
    #     main()
    # out = str(f.getvalue())
    out = ""
    for i in main():
        # print(i)
        out += i
    
    return render(request, "home.html", {"response": out})

