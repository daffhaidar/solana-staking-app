from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Wallet, StakingRecord, SolPrice
from .serializers import WalletSerializer, StakingRecordSerializer, SolPriceSerializer
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair
from solana.publickey import PublicKey
from django.conf import settings
import base58
import json
from django.utils import timezone

class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def verify_signature(self, request):
        try:
            signature = request.data.get('signature')
            message = request.data.get('message')
            public_key = request.data.get('public_key')

            # Verify the signature using Solana
            client = Client(settings.SOLANA_NETWORK)
            # Add signature verification logic here

            # Create or update wallet
            wallet, created = Wallet.objects.get_or_create(
                user=request.user,
                defaults={'address': public_key}
            )
            if not created:
                wallet.address = public_key
                wallet.save()

            return Response({
                'status': 'success',
                'wallet': self.get_serializer(wallet).data
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class StakingViewSet(viewsets.ModelViewSet):
    serializer_class = StakingRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StakingRecord.objects.filter(wallet__user=self.request.user)

    def perform_create(self, serializer):
        wallet = get_object_or_404(Wallet, user=self.request.user)
        amount = serializer.validated_data['amount']

        # Create Solana transaction for staking
        client = Client(settings.SOLANA_NETWORK)
        # Add staking transaction logic here

        # Save the staking record
        serializer.save(
            wallet=wallet,
            transaction_signature="dummy_signature"  # Replace with actual transaction signature
        )

    @action(detail=True, methods=['post'])
    def unstake(self, request, pk=None):
        staking_record = self.get_object()
        if staking_record.status != 'active':
            return Response({
                'status': 'error',
                'message': 'Staking record is not active'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create Solana transaction for unstaking
        client = Client(settings.SOLANA_NETWORK)
        # Add unstaking transaction logic here

        # Update staking record
        staking_record.status = 'completed'
        staking_record.end_time = timezone.now()
        staking_record.save()

        return Response({
            'status': 'success',
            'message': 'Unstaking successful',
            'rewards': staking_record.rewards
        })

class SolPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SolPrice.objects.all().order_by('-timestamp')
    serializer_class = SolPriceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        days = self.request.query_params.get('days', 7)
        return queryset[:int(days)] 