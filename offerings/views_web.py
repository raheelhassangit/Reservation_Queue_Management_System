from django.shortcuts import render

def dashboard_page(request):
    return render(request, "offerings/dashboard.html")

def offering_create_page(request):
    return render(request, "offerings/form.html")

def offering_edit_page(request, pk):
    return render(request, "offerings/form.html")

def offering_list_page(request):
    return render(request, "offerings/list.html")

def offering_detail_page(request, pk):
    return render(request, "offerings/detail.html")