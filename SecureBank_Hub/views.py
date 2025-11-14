from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Account, Transaction
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from .serializer import UserSerializer, AccountSerializer, TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta, datetime

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view()
def user_count(request):
    return Response({User.objects.count()})

class AccountListCreate(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_url_kwarg = {'user_id'}

    def get_queryset(self):
        queryset = super().get_queryset()
        lookup_match = False
        for x in self.lookup_url_kwarg:
            if x in self.kwargs:
                url_filter = {x: self.kwargs[x]}
                lookup_match = True
                break
        
        if lookup_match:
            queryset = queryset.filter(**url_filter)
        return queryset

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = {'pk', 'account_number'}

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_match = False
        for x in self.lookup_field:
            if x in self.kwargs:
                lookup_url_kwarg = x
                lookup_match = True

        assert lookup_match, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {lookup_url_kwarg: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

@api_view()
def account_count(request):
    return Response({Account.objects.count()})

class TransactionListCreate(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_url_kwarg = {'account_id', 'fraud_status'}

    def get_queryset(self):
        queryset = super().get_queryset()
        lookup_match = False
        for x in self.lookup_url_kwarg:
            if x in self.kwargs:
                url_filter = {x: self.kwargs[x]}
                lookup_match = True
                break
        
        if lookup_match:
            queryset = queryset.filter(**url_filter)
        return queryset

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

def HighRiskTransactions(request, threshold):
    if request.method == "GET":
        queryset = Transaction.objects.filter(fraud_score__gt=threshold).order_by("-fraud_score")
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

def RecentTransactions(request, fk):
    if request.method == "GET":
        queryset = Transaction.objects.filter(user_id=fk).filter(timestamp__gte=(datetime.now()-timedelta(hours=24))).order_by("-timestamp")
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

# def users_list(request):
#     if request.method == "GET":
#         return HttpResponse(list(User.objects.all().values()))

# def user_view(request, user_id):
#     if request.method == "GET":
#         return HttpResponse(list(User.objects.filter(id=user_id).values()))

def hello(request):
    return HttpResponse("Hello World!!!!")