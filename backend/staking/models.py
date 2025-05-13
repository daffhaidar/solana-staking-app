from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=44, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s wallet: {self.address}"

class StakingRecord(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=9)  # SOL has 9 decimal places
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    rewards = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    transaction_signature = models.CharField(max_length=88, unique=True)

    def __str__(self):
        return f"Staking record for {self.wallet.address}: {self.amount} SOL"

    def calculate_rewards(self):
        if self.status == 'active':
            duration = timezone.now() - self.start_time
            days = duration.days + (duration.seconds / 86400)  # Convert to days
            # 1% daily reward rate
            reward_rate = 0.01
            self.rewards = self.amount * reward_rate * days
            return self.rewards
        return self.rewards

class SolPrice(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    price_usd = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"SOL Price at {self.timestamp}: ${self.price_usd}" 