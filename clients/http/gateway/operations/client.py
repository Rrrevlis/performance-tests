from typing import TypedDict
from unicodedata import category

from httpx import Response, QueryParams

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


class OperationDict(TypedDict):
    """
    Структура данных операции.
    """
    id: str
    type: str
    status: str
    amount: float
    cardId: str
    category: str
    createdAt: str
    accountId: str


class OperationReceiptDict(TypedDict):
    """
    Структура данных чека по операции.
    """
    url: str
    document: str


class OperationsSummaryDict(TypedDict):
    """
    Структура данных статистики по операции.
    """
    spentAmount: float
    receivedAmount: float
    cashbackAmount: float


class GetOperationResponseDict(TypedDict):
    """
    Структура ответа на запрос информации об операции.
    """
    operation: OperationDict


class GetOperationReceiptResponseDict(TypedDict):
    """
    Структура ответа на запрос чека по операции.
    """
    receipt: OperationReceiptDict


class GetOperationsQueryDict(TypedDict):
    """
    Структура данных для получения списка операций для определенного счета.
    """
    accountId: str


class GetOperationsResponseDict(TypedDict):
    """
    Структура ответа на запрос списка операций.
    """
    operations: list[OperationDict]


class GetOperationsSummaryQueryDict(TypedDict):
    """
    Структура данных для получения статистики по операциям для определенного счета.
    """
    accountId: str


class GetOperationsSummaryResponseDict(TypedDict):
    """
    Структура ответа на запрос статистики по операциям.
    """
    summary: OperationsSummaryDict


class MakeOperationRequestDict(TypedDict):
    """
    Базовая структура данных для cоздания операции.
    """
    status: str
    amount: float
    cardId: str
    accountId: str


class MakeFeeOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции комиссии.
    """
    pass


class MakeFeeOperationResponseDict(TypedDict):
    """
    Структура ответа на запрос cоздания операции комиссии.
    """
    operation: OperationDict


class MakeTopUpOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции пополнения.
    """
    pass


class MakeTopUpOperationResponseDict(TypedDict):
    """
    Структура ответа на запрос cоздания операции пополнения.
    """
    operation: OperationDict


class MakeCashbackOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции кэшбэка.
    """
    pass


class MakeCashbackOperationResponseDict(TypedDict):
    """
    Структура ответа на запрос cоздания операции кэшбэка.
    """
    operation: OperationDict


class MakeTransferOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции перевода.
    """
    pass


class MakeTransferOperationResponseDict(TypedDict):
    """
    Структура ответа на запрос cоздания операции перевода.
    """
    operation: OperationDict


class MakePurchaseOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции покупки.
    """
    category: str


class MakePurchaseOperationResponseDict(TypedDict):
    """
    Структура ответа на запрос cоздания операции покупки.
    """
    operation: OperationDict


class MakeBillPaymentOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции оплаты по счету.
    """
    pass


class MakeBillPaymentOperationResponseDict(TypedDict):
    """
    Структура ответа на запрос cоздания операции оплаты по счету.
    """
    operation: OperationDict


class MakeCashWithdrawalOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для cоздания операции снятия наличных денег.
    """
    pass


class MakeCashWithdrawalOperationResponseDict(TypedDict):
    """
    Структура ответа на запрос cоздания операции снятия наличных денег.
    """
    operation: OperationDict


class OperationsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/operations сервиса http-gateway.
    """

    def get_operation_api(self, operation_id: str) -> Response:
        """
        Получение информации об операции по operation_id.

        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """
        Получение чека по операции по operation_id.

        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        """
        Получение списка операций для определенного счета.

        :param query: Словарь с параметрами запроса, например: {'accountId': '123'}.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get("/api/v1/operations", params=QueryParams(**query))

    def get_operations_summary_api(self, query: GetOperationsSummaryQueryDict) -> Response:
        """
        Получение статистики по операциям для определенного счета.

        :param query: Словарь с параметрами запроса, например: {'accountId': '123'}.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get("/api/v1/operations/operations-summary", params=QueryParams(**query))

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """
        Создание операции комиссии.

        :param request: Словарь с параметрами для совершаемой операции: status, amount, cardId, accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """
        Создание операции пополнения.

        :param request: Словарь с параметрами для совершаемой операции: status, amount, cardId, accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """
        Создание операции кэшбэка.

        :param request: Словарь с параметрами для совершаемой операции: status, amount, cardId, accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """
        Создание операции перевода.

        :param request: Словарь с параметрами для совершаемой операции: status, amount, cardId, accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """
        Создание операции покупки.

        :param request: Словарь с параметрами для совершаемой операции: status, amount, cardId, accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        """
        Создание операции оплаты по счету.

        :param request: Словарь с параметрами для совершаемой операции: status, amount, cardId, accountId, category.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        """
        Создание операции снятия наличных денег.

        :param request: Словарь с параметрами для совершаемой операции: status, amount, cardId, accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)

    def get_operation(self, operation_id: str) -> GetOperationResponseDict:
        """
        Получение информации об операции.

        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера (объект GetOperationResponseDict).
        """
        response = self.get_operation_api(operation_id)
        return response.json()

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseDict:
        """
        Получение чека по операции.

        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера (объект GetOperationReceiptResponseDict).
        """
        response = self.get_operation_receipt_api(operation_id)
        return response.json()

    def get_operations(self, account_id: str) -> GetOperationsResponseDict:
        """
        Получение информации об операциях по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект GetOperationsResponseDict).
        """
        query = GetOperationsQueryDict(accountId=account_id)
        response = self.get_operations_api(query)
        return response.json()

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseDict:
        """
        Получение статистики по операциям для счета.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект GetOperationsSummaryResponseDict).
        """
        query = GetOperationsSummaryQueryDict(accountId=account_id)
        response = self.get_operations_api(query)
        return response.json()

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseDict:
        """
        Создание операции комиссии.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект MakeFeeOperationResponseDict).
        """
        request = MakeFeeOperationRequestDict(
            status="COMPLETED",
            amount=55.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_fee_operation_api(request)
        return response.json()

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseDict:
        """
        Создание операции пополнения.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект MakeTopUpOperationResponseDict).
        """
        request = MakeTopUpOperationRequestDict(
            status="COMPLETED",
            amount=100.33,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_top_up_operation_api(request)
        return response.json()

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponseDict:
        """
        Создание операции кэшбэка.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект MakeCashbackOperationResponseDict).
        """
        request = MakeCashbackOperationRequestDict(
            status="COMPLETED",
            amount=30.15,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_cashback_operation_api(request)
        return response.json()

    def make_transfer_operation(self, card_id: str, account_id: str) -> MakeTransferOperationResponseDict:
        """
        Создание операции перевода.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект MakeTransferOperationResponseDict).
        """
        request = MakeTransferOperationRequestDict(
            status="COMPLETED",
            amount=204.67,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_transfer_operation_api(request)
        return response.json()

    def make_purchase_operation(self, card_id: str, account_id: str) -> MakePurchaseOperationResponseDict:
        """
        Создание операции покупки.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект MakePurchaseOperationResponseDict).
        """
        request = MakePurchaseOperationRequestDict(
            status="COMPLETED",
            amount=576.02,
            cardId=card_id,
            accountId=account_id,
            category="cinema"
        )
        response = self.make_purchase_operation_api(request)
        return response.json()

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> MakeBillPaymentOperationResponseDict:
        """
        Создание операции оплаты по счету.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект MakeBillPaymentOperationResponseDict).
        """
        request = MakeBillPaymentOperationRequestDict(
            status="COMPLETED",
            amount=2034.07,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_bill_payment_operation_api(request)
        return response.json()

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> MakeCashWithdrawalOperationResponseDict:
        """
        Создание операции снятия наличных денег.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект MakeCashWithdrawalOperationResponseDict).
        """
        request = MakeCashWithdrawalOperationRequestDict(
            status="COMPLETED",
            amount=5000.00,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return response.json()


def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Функция создаёт экземпляр OperationsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию OperationsGatewayHTTPClient.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())
