from django.shortcuts import render_to_response

__author__ = 'bulat.fattahov'

def block(request):
    return render_to_response('block.html')


def json(request):
    operation = request.data.operation


    pass