from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def upload(request):
    context = { "status": False }
    
    try:
        if request.method == 'POST' and request.FILES['file']:
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
        
            context["url"] = fs.url(filename)
            context["message"] = "File has been uploaded successfully"
            context["status"] = True
        else:
            context["message"] = "Either no file received or invalid request method"
    except Exception as e:
        context["message"] = "Exception occured {}".format(str(e))

    return render(request, 'pages/upload.html', context)