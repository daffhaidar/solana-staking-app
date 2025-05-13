from rest_framework import serializers
from .models import Wallet, StakingRecord, SolPrice

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['address', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class StakingRecordSerializer(serializers.ModelSerializer):
    wallet_address = serializers.CharField(source='wallet.address', read_only=True)
    current_rewards = serializers.SerializerMethodField()

    class Meta:
        model = StakingRecord
        fields = [
            'id', 'wallet_address', 'amount', 'start_time', 'end_time',
            'status', 'rewards', 'transaction_signature', 'current_rewards'
        ]
        read_only_fields = ['start_time', 'end_time', 'rewards', 'transaction_signature']

    def get_current_rewards(self, obj):
        return obj.calculate_rewards()

class SolPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolPrice
        fields = ['timestamp', 'price_usd']
        read_only_fields = ['timestamp'] 