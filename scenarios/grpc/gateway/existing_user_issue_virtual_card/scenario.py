from locust import task, events
from locust.env import Environment

from clients.grpc.gateway.locust import GatewayGRPCTaskSet
from seeds.scenarios.existing_user_issue_virtual_card import ExistingUserIssueVirtualCardSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


# Этот хук выполняется один раз при инициализации теста (до старта пользователей).
# Мы используем его, чтобы заранее прогнать сидинг и загрузить пользователей в память.
@events.init.add_listener
def init(environment: Environment, **kwargs):
    # Создаем экземпляр сидинг-сценария
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()

    # Выполняем генерацию данных, если они ещё не созданы
    seeds_scenario.build()

    # Загружаем сгенерированных пользователей в окружение Locust
    environment.seeds = seeds_scenario.load()


class IssueVirtualCardTaskSet(GatewayGRPCTaskSet):
    """
    Нагрузочный сценарий, который:
    1. Запрашивает список счетов (несколько раз)ю
    2. Выпускает виртуальную карту для существующего дебетового счета.

    Использует базовый GatewayGRPCTaskSet и уже созданных в нём API клиентов.
    """
    # Типизируем объект пользователя из сидинга
    seed_user: SeedUserResult

    # Метод вызывается при запуске каждой сессии пользователя (до начала задач)
    def on_start(self) -> None:
        super().on_start()

        # Получаем случайного пользователя из списка
        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(2)
    def get_accounts(self):
        """
        Запрашиваем список счетов.
        """
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(1)
    def issue_virtual_card(self):
        """
        Выпускаем виртуальную карту.
        """
        self.cards_gateway_client.issue_virtual_card(
            user_id=self.seed_user.user_id,
            account_id=self.seed_user.debit_card_accounts[0].account_id
        )


class IssueVirtualCardScenarioUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий сценарий выпуска виртуальной карты.
    """
    tasks = [IssueVirtualCardTaskSet]
