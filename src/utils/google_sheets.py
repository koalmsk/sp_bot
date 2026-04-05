import gspread


class googleSheet:
    def __init__(self):
        self.gc = gspread.service_account(filename="cread.json")
        self.wks = self.gc.open_by_url(
            "https://docs.google.com/spreadsheets/d/172GQNWe5ncmpejoaufUCQgP_3yL6p8YGR6-a3Zv2pBA/edit?gid=0#gid=0"
        ).sheet1

    def add_order(
        self,
        tg_id: str,
        tg_link: str,
        poizon_link,
        poizon_name,
        size: str,
        y_price,
        currency,
        rub_price,
        delivery_mode,
    ):
        order_code = str(tg_id + str(len(self.wks.findall(tg_id))))

        self.wks.append_row(
            [
                tg_id,
                tg_link,
                poizon_link,
                poizon_name,
                size,
                y_price,
                currency,
                rub_price,
                delivery_mode,
                order_code,
                "Не оплачен",
                "Нет комментов от админа",
            ]
        )
        return order_code

    def get_order(self, order_code):
        row = self.wks.find(order_code).row
        order_data = self.wks.get(f"A{row}:L{row}")[0]

        order_data_dict = {
            "poizon_link": order_data[3],
            "poizon_name": order_data[2],
            "size": order_data[4],
            "price_ru": order_data[7],
            "delivery_mode": order_data[8],
            "order_code": order_data[9],
            "status": order_data[10],
            "comment": order_data[11],
        }
        return order_data_dict
