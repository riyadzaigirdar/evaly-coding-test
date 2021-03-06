import os
import pandas as pd
from loans.models import Loan
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status, viewsets
from loans.serializers import LoanSerializer, LoanListSerializer


class LoanView(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            # admins will see all loan request list
            serializer = LoanListSerializer(Loan.objects.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # members will set own loan request list
            serializer = LoanListSerializer(Loan.objects.filter(
                member__id=request.user.id), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        # only members can create/request for loans
        if not request.user.is_member:
            return Response({"message": "only members can create/request for loans"}, status=status.HTTP_403_FORBIDDEN)
        body = {
            "member": request.user.id,
            **request.data
        }
        serializer = LoanSerializer(data=body)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, partial=False):
        # only admin will be able to update a loan request
        if not request.user.is_superuser:
            return Response({"message": "only admin will be able to update a loan request"}, status=status.HTTP_403_FORBIDDEN)

        serializer = LoanSerializer(Loan.objects.get(id=pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        obj = Loan.objects.get(id=kwargs["pk"])
        # the member who created that loan request or admin can delete the loan loan request
        if request.user.is_superuser or request.user.id == obj.member.id:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"message": "you didn't create the loan request or you are not admin"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_excel_for_loans(request):
    loan_ids = []
    member_ids = []
    member_names = []
    book_names = []
    book_ids = []
    is_accepted = []
    is_rejected = []
    is_returned = []
    for obj in Loan.objects.all():
        loan_ids.append(obj.id)
        member_ids.append(obj.member.id)
        member_names.append(obj.member.name)
        book_names.append(obj.book.name)
        book_ids.append(obj.book.id)
        is_accepted.append(obj.is_accepted)
        is_rejected.append(obj.is_rejected)
        is_returned.append(obj.is_returned)

    dataframe = {
        "loan_id": loan_ids,
        "member_id": member_ids,
        "member_name": member_names,
        "book_name": book_names,
        "book_id": book_ids,
        "is_accepted": is_accepted,
        "is_rejected": is_rejected,
        "is_returned": is_returned
    }
    csv_converter = pd.DataFrame(dataframe)
    csv_converter.to_csv("media/loans.csv", index=False)

    return Response({"download_link": f"{settings.MEDIA_URL}loans.csv"}, status=status.HTTP_200_OK)
