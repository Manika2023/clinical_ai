from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.agents import run_agent


class TrialQueryAPI(APIView):
    def post(self, request):
        query = request.data.get("query")
        print("query is",query)  
        if not query:
            return Response({"error": "Query field is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print("try occured")
            result = run_agent(query)
            print("RAW DATA:", result)
            return Response(
                {
                    "query": query,
                    "answer": result
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("else occured")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
