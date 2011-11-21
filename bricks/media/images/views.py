from django.views.generic import list_detail
from .models import Image

def image_detail(request, object_id):
    queryset = Image.objects.all()
    return list_detail.object_detail(request, queryset, object_id=object_id,
                                     template_name='images/image_detail.html')
