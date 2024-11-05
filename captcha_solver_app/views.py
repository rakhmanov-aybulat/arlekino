import base64

import cv2
import numpy
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from captcha_solver_app.solver import get_solved_image


def index(request) -> HttpResponse:
    return render(request, 'captcha_solver_app/index.html')


@csrf_exempt
def solve_captcha(request: HttpRequest):
    if request.method == 'POST':
        data = request.POST
        image_data = data.get('image')
        objects_to_detect = data.get('objects')

        if not isinstance(image_data, str):
            raise ValueError()

        if not isinstance(objects_to_detect, str):
            raise ValueError()

        image = base64.b64decode(image_data)
        image_as_np = numpy.frombuffer(image, dtype=numpy.uint8)
        image = cv2.imdecode(image_as_np, flags=1)


        solved_image, objects_count = \
                get_solved_image(image, objects_to_detect)

        _, solved_image_array = cv2.imencode('.png', solved_image)
        solved_image_bytes = solved_image_array.tobytes()

        solved_image_data = \
                base64.b64encode(solved_image_bytes).decode('utf-8')

        return JsonResponse({'image': solved_image_data,
                             'objectsCount': objects_count})

