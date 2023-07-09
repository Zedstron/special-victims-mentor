from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from .pdfhandler import GetResult

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
            context["message"] = GetResult("./media/{}".format(filename), "VertexAI")
            context["status"] = True if context["message"] else False
        else:
            context["message"] = "Either no file received or invalid request method"
        # context["message"] = [{"title":"File a police report","start":"2023-05-01","end":"2023-05-15","description":"Contact the police department in the city where the incident occurred and file a police report. Be sure to bring any evidence you have, such as photos or witness statements.","institution":"Police department","instructions":"Tell the police officer what happened and provide any evidence you have. The officer will file a police report and give you a copy.","deadline":"2023-05-15"},{"title":"File a restraining order","start":"2023-05-16","end":"2023-06-15","description":"Contact the courthouse in the county where the incident occurred and file a restraining order. Be sure to bring any evidence you have, such as photos or witness statements.","institution":"Courthouse","instructions":"Tell the clerk what happened and provide any evidence you have. The clerk will file a restraining order and give you a copy.","deadline":"2023-06-15"},{"title":"File a civil lawsuit","start":"2023-06-16","end":"2023-12-31","description":"Contact a lawyer and file a civil lawsuit against the person who assaulted you. Be sure to bring any evidence you have, such as photos or witness statements.","institution":"Lawyer","instructions":"Tell the lawyer what happened and provide any evidence you have. The lawyer will file a civil lawsuit on your behalf.","deadline":"2023-12-31"}]
    except Exception as e:
        context["message"] = "Exception occured {}".format(str(e))

    return render(request, 'pages/upload.html', context)