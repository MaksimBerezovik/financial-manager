# Тут обрабатываем данные и выводим статистику по раходам и доходам
from bot import BotDB


def command_processing(message: str, user_id):
    cmd_variants = ("!statistic", "/statistic", "!статистика", "/статистика")
    within_als = {
        "day": ("today", "day", "сегодня", "день"),
        "month": ("month", "месяц"),
        "year": ("year", "год"),
    }
    expenses, income = 0, 0
    cmd = message
    for r in cmd_variants:
        cmd = cmd.replace(r, "").strip()
    within = "month"
    if len(cmd):
        for i in within_als:
            for j in within_als[i]:
                if j == cmd:
                    within = cmd

    records = BotDB.get_records(user_id, within)  # get records
    # считаем сумму расходов и доходов
    for rec in records:
        if not rec[2]:
            expenses += rec[3]  # расходы
        else:
            income += rec[3]  # доходы
    if within == "month":
        within = "месяц"
    result = (expenses * 100) / income
    if result > 0.5:
        result = round(result, 1)
    else:
        result  = round(result, 5)
    return f"Расходы составили {result} %  от доходов за {within}"


def get_statistic(message: str, user_id: int):
    answer = command_processing(message, user_id)
    return answer
