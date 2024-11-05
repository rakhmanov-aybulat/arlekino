from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import io
from PIL import Image


def index(request) -> HttpResponse:
    return render(request, 'captcha_solver_app/index.html')


@csrf_exempt
def solve_captcha(request):
    if request.method == 'POST':
        data = request.POST
        image_data = data.get('image')

        objects_to_detect = data.get('objects')
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        solved_image = Image.open(r'/path/to/image/image.png')

        buffer = io.BytesIO()
        solved_image.save(buffer, format='PNG')
        solved_image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return JsonResponse({'image': solved_image_data})

