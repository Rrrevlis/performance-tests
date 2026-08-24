from locust import task

from clients.grpc.gateway.locust import GatewayGRPCSequentialTaskSet
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse
from tools.locust.user import LocustBaseUser


class IssuePhysicalCardSequentialTaskSet(GatewayGRPCSequentialTaskSet):
    """
    Нагрузочный сценарий, который последовательно:
    1. Создаёт нового пользователя.
    2. Открывает дебетовый счёт.
    3. Выпускает физическую карту, привязанную к этому счёту.

    Использует базовый GatewayGRPCSequentialTaskSet и уже созданных в нём API клиентов.
    """

    create_user_response: CreateUserResponse | None = None
    open_debit_card_account_response: OpenDebitCardAccountResponse | None = None

    @task
    def create_user(self):
        """
        Создаём нового пользователя и сохраняем результат для последующих шагов.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        """
        Открываем дебетовый счёт для созданного пользователя.
        Проверяем, что предыдущий шаг был успешным.
        """
        if not self.create_user_response:
            return

        self.open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def issue_physical_card(self):
        """
        Выпускаем физическую карту, если счёт был успешно открыт.
        """
        if not self.open_debit_card_account_response:
            return

        self.cards_gateway_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_debit_card_account_response.account.id
        )


class IssuePhysicalCardScenarioUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий последовательный сценарий выпуска физической карты.
    """
    tasks = [IssuePhysicalCardSequentialTaskSet]
