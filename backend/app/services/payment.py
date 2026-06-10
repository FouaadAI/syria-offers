from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class PaymentMethod(str, Enum):
    SHAM_CASH = "sham_cash"
    MTN_CASH = "mtn_cash"
    SYRIATEL_CASH = "syriatel_cash"


class PaymentRequest(BaseModel):
    amount: float
    phone: str
    method: PaymentMethod
    booking_id: int


class PaymentResponse(BaseModel):
    success: bool
    transaction_id: str
    message: str


class PaymentProvider(ABC):
    @abstractmethod
    async def process_payment(self, payment: PaymentRequest) -> PaymentResponse:
        pass


class ApiSyriaProvider(PaymentProvider):
    """
    Stub provider for future API Syria integration:
    - ShamCash
    - MTN Cash
    - Syriatel Cash
    """

    async def process_payment(self, payment: PaymentRequest) -> PaymentResponse:
        prefix_map = {
            PaymentMethod.SHAM_CASH: "SHAM",
            PaymentMethod.MTN_CASH: "MTN",
            PaymentMethod.SYRIATEL_CASH: "SYR",
        }
        label_map = {
            PaymentMethod.SHAM_CASH: "Sham Cash",
            PaymentMethod.MTN_CASH: "MTN Cash",
            PaymentMethod.SYRIATEL_CASH: "Syriatel Cash",
        }
        prefix = prefix_map[payment.method]
        label = label_map[payment.method]
        return PaymentResponse(
            success=True,
            transaction_id=f"{prefix}-{payment.booking_id}-{int(datetime.now().timestamp())}",
            message=f"Payment processed successfully via {label}",
        )


class PaymentGateway:
    def __init__(self, provider: PaymentProvider | None = None):
        self.provider = provider or ApiSyriaProvider()

    async def process_payment(self, payment: PaymentRequest) -> PaymentResponse:
        return await self.provider.process_payment(payment)
