import csv
import io
import json
from django.apps import apps
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.http import HttpResponse
from utils import create_download_response, create_excel_response, get_model, get_serializer, list_all_models
from openpyxl import Workbook
from rest_framework.renderers import JSONRenderer

class DataDownloadViewSet(viewsets.ViewSet):
    
    def list(self, request):
        return Response({"message": "Specify the model name and format in the URL."}, status=status.HTTP_200_OK)
    
    # url_path=r'download/(?P<model_name>[^/.]+)/(?P<file_format>[^/.]+)')
    @action(detail=False, methods=['get'], url_path=r'download/(?P<app_label>[^/.]+)/(?P<model_name>[^/.]+)/(?P<file_format>[^/.]+)')
    def download_data(self, request, app_label=None, model_name=None, file_format=None):
        try:
            model = apps.get_model(app_label, model_name)  # Get the model class
            serializer_class = get_serializer(model)
            queryset = model.objects.all()
            serializer = serializer_class(queryset, many=True)
            data = serializer.data


            if file_format == 'json':
                serializer = serializer_class(queryset, many=True)
                data = serializer.data
                
                # Serialize the data to JSON
                formatted_data = json.dumps(serializer.data, indent=4)

                # Set the Content-Disposition header to force download
                response = HttpResponse(formatted_data, content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename="{model_name}.json"'
                return response

            elif file_format == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'

                writer = csv.writer(response)
                if data:
                    header = data[0].keys()
                    writer.writerow(header)
                    for item in data:
                        writer.writerow(item.values())

                return response

            elif file_format == 'excel':
                serializer = serializer_class(queryset, many=True)
                data = serializer.data
                return create_excel_response(data, filename='data.xlsx')


            else:
                return Response({"error": "Unsupported format"}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def list_models(request):
    models = list_all_models()
    return Response(models, status=status.HTTP_200_OK)



#-----------------------
# views.py

from django.http import HttpResponse

def download_json_view(request):
    data = request.GET.get('data', '')  # Get the JSON data from the request parameters
    # You can modify the response headers as needed
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="data.json"'
    return response



#-------for upload-------------