from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json

class VoucherView(APIView):
    def post(self, request):
        voucher_value = request.data.get('voucher_value')

        if not voucher_value.strip():
            return Response({'error': 'Voucher value is required'}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://service.alignbooks.com/ABReportService.svc/GetReportData"
        payload = {
                    "report_type":4444,
                        "filter_data":{
                            "period_from":{
                                "name":"Date_From",
                                "applicable":True,
                                "caption":"Period",
                                "master_list_type":0,
                                "multi_select":True,
                                "value":"2024-05-24 00:11:00"
                            },
                            "period_to":{
                                "name":"Date_To",
                                "applicable":True,
                                "caption":"Period",
                                "master_list_type":0,
                                "multi_select":True,
                                "value":"2024-05-24 00:11:00"
                            },
                            "Pending":{
                                "name":"Combo_Pending",
                                "applicable":False,
                                "caption":"",
                                "master_list_type":0,
                                "multi_select":True,
                                "value":"2"
                            },
                            "txt_misc_1":{
                                "name":"Text_VoucherNo",
                                "applicable":True,
                                "caption":"",
                                "master_list_type":0,
                                "multi_select":False,
                                "value":voucher_value
                            },
                            "location":{
                                "name":"Text_VoucherNo",
                                "applicable":False,
                                "caption":"",
                                "master_list_type":0,
                                "multi_select":True,
                                "value":""
                            }
                        }
                    }
        headers =  {"username": "narayananbkr@gmail.com" ,
                     "apikey": "db43745e-9890-11ee-b041-005056a52680" ,
                     "company_id": "2a686e75-2e22-4147-8c61-1c0ebcb2f517" ,
                     "enterprise_id": "e4063c5d-79c1-49de-aef1-7fcbcd0a9eb2" ,
                     "user_id": "4861b274-0ed1-4632-a34b-1a2ec16c45f0" ,
                     "Content-Type": "application/json"} 

        try:
                api_response = requests.post(url, data=json.dumps(payload), headers=headers)
                api_response.raise_for_status()
        except requests.exceptions.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        response_data = api_response.json()
        json_data_table = None
        extracted_values = []
        if response_data:
              if response_data["JsonDataTable"]:
                    json_data_table = json.loads(response_data["JsonDataTable"])
                    extracted_values.append({
                    'party': json_data_table[0]["Party"],
                    'delivery_date':json_data_table[0]["delivery_date"],  
                    'invoice_no' : json_data_table[0]["invoice_no"]                   
                })
        return Response(extracted_values, status=status.HTTP_200_OK)        
              
      