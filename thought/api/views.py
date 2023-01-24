from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .serializers import ThoughtSerializer
from django.utils.timezone import now

import requests
import json

"""
view for thought of the day
"""
class Thought(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]

    def list(self, request):
        # get thoyght from api ninjas.com
        category = 'learning'
        api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
        try:
            response = requests.get(api_url, headers={'X-Api-Key': 'XfllCBPmFtOTrmXNHg6EZQ==EBINPUjfGwcgI1cg'})
        except:
            return Response({"message": "Some error occured"}, status=status.HTTP_204_NO_CONTENT)

        if response.status_code == requests.codes.ok:
            str_data = json.dumps(response.json())
            json_data = json.loads(str_data)

            # retrieve quote and author
            quote = json_data[0]['quote']
            author = json_data[0]['author']

            data = {
                    'quote':quote,
                    'author':author,
                    }

            serializer = ThoughtSerializer(data)

            data = serializer.data
            data['date']=now().date()  # add date

            return Response(data, status=status.HTTP_200_OK)
            
        return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)