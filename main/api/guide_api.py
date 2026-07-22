def status_codes(key):
    data = {
        "EMITTED" : "Эмитирован",
        "APPLIED": "Нанесён",
        "INTRODUCED": "В обороте",
        "WRITTEN_OFF": "Списан",
        "RETIRED": "Выбыл",
        "WITHDRAWN": "Выбыл",
        "DISAGGREGATION": "Расформирован",
        "DISAGGREGATED": "Расформирован",
        "APPLIED_NOT_PAID": "Не оплачен",
        "IN_GRAY_ZONE": "В Серой зоне",
        "EMPTY": "Значение отсутствует",
        "RESERVED_NOT_USED": "Зарезервировано.Не использовать",
        "INDIVIDUAL": "КиЗ индивидуализирован",
        "NON_INDIVIDUAL": "Не индивидуализирован",
        "WAIT_SHIPMENT": "Ожидает приёмку товара",
        "EXPORTED": "Используется для документов экспорта",
        "LOAN_RETIRED": "Выведен из оборота по договору рассрочки",
        "LOST_INVENTORY": "Не найдены по итогу инвентаризации",
        "REMARK_RETIRED": "Перемаркирован",
        "WAIT_TRANSFER_TO_OWNER" : "Ожидает передачу собственнику",
        "WAIT_REMARK": "Ожидает перемаркировку",
        "RETIRED_CANCELLATION": "Списан / Аннулирован",
        "FTS_RESPOND_NOT_OK": "Отрицательное решение ФТС",
        "FTS_RESPOND_WAITING": "Ожидает подтверждение ФТС",
        "FTS_CONTROL": "На контроле ФТС",
        "EAS_RESPOND_NOT_OK": "Отрицательное решение ЕАЭС",
        "EAS_RESPOND_WAITING": "Ожидает подтверждение ЕАЭС",
        "CONNECT_TAP": "Подключён к оборудованию для розлива",
        "PRIM_RESPONSE_WAITING" :"Обрабатывается",
        "MOVING_BY_UD": "Отгружен",
    }
    try:
        request_data = data[key]
    except KeyError:
        request_data = ""
    return request_data

def types_of_packaging(key):
    data = {
        "UNIT": "Единица товара",
        "GROUP": "Групповая упаковка",
        "SET": "Набор",
        "BUNDLE": "Комплект",
        "BOX": "Транспортная упаковка",
        "ATK": "Агрегированный таможенный код",
        "LEVEL1": "Транспортная упаковка 1-го уровня",
    }
    try:
        request_data = data[key]
    except KeyError:
        request_data = ""
    return request_data