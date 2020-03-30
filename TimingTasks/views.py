from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from TimingTasks import index_analysis_task

@require_http_methods(["GET"])
def calc_index_analysis_info(request):
    response = {}
    response['result'] = index_analysis_task.calc_index_analysis_info()

    return JsonResponse(response)