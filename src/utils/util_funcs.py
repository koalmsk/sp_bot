from dotenv import load_dotenv
from os import getenv
from bot_initer.bot_init import bot



def check_admin(user_id: str) -> bool:
    load_dotenv()
    a = [getenv(f"admin{index}") for index in range(3)]
    print(a)
    return str(user_id) in a


def calculate_price(price_china, data: dict) -> int:
    cost = 0
    rubles = price_china * data["currency"]

    if price_china < data["down"]["limit"]:
        cost = rubles + data["down"]["profit"]

    elif data["down"]["limit"] <= price_china < data["up"]["limit"]:
        cost = rubles + data["up"]["profit"]

    elif price_china >= data["up"]["limit"]:
        cost = rubles + (rubles * (data["percentage"] / 100))

    return int(cost)


async def notification_to_admin(text):
    load_dotenv()
    admin_list = [getenv(f"admin{index}") for index in range(3)]
    for admin_id in admin_list:
        try:
            await bot.send_message(admin_id, text, parse_mode="Markdown")
            print(f"Сообщение отправлено пользователю {admin_id}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
