from django.shortcuts import render


def first_plot(request):
    return render(request, 'graph.html')
