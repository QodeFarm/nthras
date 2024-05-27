import csv
from django.http import HttpResponse
import json
import openpyxl
from openpyxl.utils import get_column_letter
from .fields import *
   

class StripDownloadJsonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store the original path
        original_path = request.path_info
 

        #------------ J S O N ------------------------------------

        if original_path.endswith('download/json/'):
            # Strip the '/download/json/' part from the URL
            modified_path = original_path[:-len('download/json/')]
            # Modify both path and path_info
            request.path_info = modified_path
            request.path = modified_path
            request.download_json = True
        else:
            request.download_json = False

        # Get the response from the next middleware or view
        response = self.get_response(request)
        
        # Restore the original path_info to avoid affecting other middlewares or views
        request.path_info = original_path
        request.path = original_path


        # If the original request URL ended with '/download/json/'
        if getattr(request, 'download_json', False):
            # Ensure the response is JSON
            print('response.status_code = ',response.status_code)
            print('content-type = ',response['Content-Type'])
            if response.status_code == 200: # and 'application/json' in response['Content-Type']:

                try:
                    content = response.content
                    data = content.decode('utf-8')
                    data = response.data

                except json.JSONDecodeError:
                    return response  # Return the original response if JSON decoding fails

                # Return the data as a downloadable JSON file
                response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="Json_data_file.json"'
                return response
            
        #-------------- C S V -------------------------------------

        if original_path.endswith('download/csv/'):
            # Strip the '/download/csv/' part from the URL
            modified_path = original_path[:-len('download/csv/')]
            # Modify both path and path_info
            request.path_info = modified_path
            request.path = modified_path
            request.download_csv = True
        else:
            request.download_csv = False

        # Get the response from the next middleware or view
        response = self.get_response(request)
        
        # Restore the original path_info to avoid affecting other middlewares or views
        request.path_info = original_path
        request.path = original_path

        # If the original request URL ended with '/download/csv/'
        if getattr(request, 'download_csv', False):
            # Ensure the response is JSON
            print('response.status_code = ',response.status_code)
            print('content-type = ',response['Content-Type'])
            if response.status_code == 200:

                try:
                    content = response.content
                    data = content.decode('utf-8') #decode the data in content
                    data = response.data
                    extracted_data = (data['data'])
                    

        
                    response = HttpResponse(json.dumps(extracted_data, indent=2), content_type='application/json')
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="csv_data_file.csv"'

                    writer = csv.writer(response)
                    if data:
                        header = extracted_data[0].keys()
                        writer.writerow(header)
                        for item in extracted_data:
                            writer.writerow(item.values())

                    return response   

                except json.JSONDecodeError:
                    return response  # Return the original response if JSON decoding fails 

        #------------ E X C E L --------------------------------------                 

        if original_path.endswith('download/excel/'):
            # Strip the '/download/excel/' part from the URL
            modified_path = original_path[:-len('download/excel/')]
            # Modify both path and path_info
            request.path_info = modified_path
            request.path = modified_path
            request.download_excel = True
        else:
            request.download_excel = False

        # Get the response from the next middleware or view
        response = self.get_response(request)
        
        # Restore the original path_info to avoid affecting other middlewares or views
        request.path_info = original_path
        request.path = original_path

        # If the original request URL ended with '/download/excel/'
        if getattr(request, 'download_excel', False):
            # Ensure the response is JSON
            print('response.status_code = ',response.status_code)
            print('content-type = ',response['Content-Type'])
            if response.status_code == 200: # and 'application/json' in response['Content-Type']:

                try:
                    content = response.content
                    data = content.decode('utf-8') #decode the data in content
                    data = response.data
                    extracted_data = (data['data'])
        
                    # dict_data = json.loads(json_data)
                    response = HttpResponse(json.dumps(extracted_data, indent=2), content_type='application/json')
                except json.JSONDecodeError:
                    return response  # Return the original response if JSON decoding fails
                else: 
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="csv_data_file.csv"'

                    writer = csv.writer(response)
                    wb = openpyxl.Workbook()
                    ws = wb.active
                    ws.title = "Data"

                    if data:
                        # Write the headers
                        header = extracted_data[0].keys()
                        writer.writerow(header)
                        for col_num, header in enumerate(header, 1):
                            col_letter = get_column_letter(col_num)
                            ws[f'{col_letter}1'] = header

                        # Write the data rows
                        for row_num, item in enumerate(extracted_data, 2):
                            for col_num, (key, value) in enumerate(item.items(), 1):
                                col_letter = get_column_letter(col_num)
                                ws[f'{col_letter}{row_num}'] = str(value)  # Convert value to string

                            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    response['Content-Disposition'] = f'attachment; filename="excel_data_file.xlsx"'
                    wb.save(response)

                    return response
        
        return response # This will return original response as it is.