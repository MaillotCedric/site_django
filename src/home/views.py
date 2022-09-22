from django.shortcuts import render

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home/public.html')
    return render(request, 'home/private.html')