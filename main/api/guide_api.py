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


def types_of_emission(key):
    data = {
        "LOCAL": "Производство РФ",
        "FOREIGN": "Ввезён в РФ",
        "REMAINS": "Маркировка остатков",
        "CROSSBORDER": "Ввезён из стран ЕАЭС",
        "REMARK": "Перемаркировка",
        "COMMISSION": "Принят на комиссию от физического лица",
        "REAPPLY": "Маркировка вне производства или импорта",
    }
    try:
        request_data = data[key]
    except KeyError:
        request_data = ""
    return request_data

def product_groups(key):
    data = {
        "lp": {"id" :1, "description" : "Лёгкая промышленность"},
        "shoes": {"id": 2, "description": "Обувные товары"},
        "tobacco": {"id": 3, "description": "Табачная продукция"},
        "perfumery": {"id": 4, "description": "Духи и туалетная вода"},

        "tires": {"id": 5, "description": "Шины и покрышки пневматические резиновые новые"},
        "electronics": {"id": 6, "description": "Фотокамеры (кроме кинокамер), фотовспышки и лампы-вспышки"},
        "milk": {"id": 8, "description": "Молочная продукция"},
        "bicycle": {"id": 9, "description": "Велосипеды и велосипедные рамы"},

        "wheelchairs": {"id": 10, "description": "Медицинские изделия"},
        "alcohol": {"id": 11, "description": "Алкоголь"},
        "otp": {"id": 12, "description": "Альтернативная табачная продукция"},
        "water": {"id": 13, "description": "Упакованная вода"},

        "furs": {"id": 14, "description": "Товары из натурального меха"},
        "beer": {"id": 15, "description": "Пиво, напитки, изготавливаемые на основе пива, слабоалкогольные напитки"},
        "ncp": {"id": 16, "description": "Никотиносодержащая продукция"},
        "bio": {"id": 17, "description": "Специализированная пищевая продукция и БАД к пище"},

        "antiseptic": {"id": 19, "description": "Антисептики и дезинфицирующие средства"},
        "petfood": {"id": 20, "description": "Корма для животных"},
        "seafood": {"id": 21, "description": "Морепродукты"},
        "nabeer": {"id": 22, "description": "Безалкогольное пиво"},

        "softdrinks": {"id": 23, "description": "Соковая продукция и безалкогольные напитки"},
        "meat": {"id": 25, "description": "Мясные изделия"},
        "vetpharma": {"id": 26, "description": "Ветеринарные препараты"},
        "toys": {"id": 27, "description": "Игры и игрушки для детей"},

        "radio": {"id": 28, "description": "Радиоэлектронная продукция"},
        "titan": {"id": 31, "description": "Титановая металлопродукция"},
        "conserve": {"id": 32, "description": "Консервированная продукция"},
        "vegetableoil": {"id": 33, "description": "Растительные масла"},

        "opticfiber": {"id": 34, "description": "Оптоволокно и оптоволоконная продукция"},
        "chemistry": {"id": 35, "description": "Косметика, бытовая химия и товары личной гигиены"},
        "books": {"id": 36, "description": "Печатная продукция"},
        "grocery": {"id": 37, "description": "Бакалейная продукция"},

        "pharmaraw": {"id": 38, "description": "Фармацевтическое сырьё, лекарственные средства"},
        "construction": {"id": 39, "description": "Строительные материалы"},
        "fire": {"id": 40, "description": "Пиротехника и огнетушащее оборудование"},
        "heater": {"id": 41, "description": "Отопительные приборы"},

        "cableraw": {"id": 42, "description": "Кабельно-проводниковая продукция"},
        "autofluids": {"id": 43, "description": "Моторные масла"},
        "polymer": {"id": 44, "description": "Полимерные трубы"},
        "sweets": {"id": 45, "description": "Сладости и кондитерские изделия"},

        "carparts": {"id": 48, "description": "Автозапчасти и комплектующие транспортных средств"},
        "furslp": {"id": 49, "description": "Натуральный мех"},
        "nicotindev": {"id": 50, "description": "Радиоэлектронная продукция. Электронные системы доставки никотина"},
        "gadgets": {"id": 51, "description": "Радиоэлектронная продукция. Ноутбуки и смартфоны"},

        "frozen": {"id": 52, "description": "Полуфабрикаты и замороженные продукты"},
        "fertilizers": {"id": 53, "description": "Удобрения в потребительской упаковке"},
        "homeware": {"id": 54, "description": "Товары для дома и интерьера"},
        "pyrotechnics": {"id": 59, "description": "Пиротехнические изделия"},

    }
    try:
        request_data = data[key]
    except KeyError:
        request_data = ""
    return request_data

