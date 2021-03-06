from loans import models
from django.contrib.auth import get_user_model
from rest_framework import serializers
from books.serializers import BookListSerializer


class LoanMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email']


class LoanListSerializer(serializers.ModelSerializer):
    member = LoanMemberSerializer()

    class Meta:
        model = models.Loan
        fields = ['id', 'member', 'book', 'is_accepted', 'is_rejected',
                  'is_returned']


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Loan
        fields = ['id', 'member', 'book', 'is_accepted', 'is_rejected',
                  'is_returned']
        extra_kwargs = {'member': {'required': False},
                        'book': {'required': False}}
