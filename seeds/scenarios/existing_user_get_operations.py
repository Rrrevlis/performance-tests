from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedCardsPlan, \
    SeedAccountsPlan, SeedOperationsPlan


class ExistingUserGetOperationsSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который загружает список своих счетов,
    затем загружает список операций по своему кредитному счёту и просматривает статистику
    по этим операциям.
    Создаёт 300 пользователей, открывает кредитный счёт и совершает операции покупки,
    пополнения счёта и снятия наличных.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        План сидинга, который описывает, сколько пользователей нужно создать
        и какие именно данные для них генерировать.
        В данном случае создаём 300 пользователей, каждому даём кредитный счёт и совершаем
        5 операций покупки, 1 операцию пополнения счёта и 1 операцию снятия наличных.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Количество пользователей
                credit_card_accounts=SeedAccountsPlan(
                    count=1,  # Количество счётов на пользователя
                    purchase_operations=SeedOperationsPlan(count=5),  # Количество операций покупки
                    top_up_operations=SeedOperationsPlan(count=1),  # Количество операций пополнения счёта
                    cash_withdrawal_operations=SeedOperationsPlan(count=1)  # Количество операций снятия наличных
                )
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Название сценария сидинга, которое будет использоваться для сохранения данных.
        """
        return "existing_user_get_operations"


if __name__ == '__main__':
    # Если файл запускается напрямую, создаём объект сценария и запускаем его.
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()  # Стартуем процесс сидинга
