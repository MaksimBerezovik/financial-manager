from aiogram import types
import statistic
from dispatcher import dp
import re
from bot import BotDB
import datetime
from handlers.courses import *


def data_format(data):
    data_time = datetime.datetime.strptime(
        data, "%Y-%m-%d %H:%M:%S"
    )  # transform into class datatime
    data_formated = datetime.datetime.strftime(
        data_time, "%d-%m-%Y %H:%M"
    )  # transform into formated data <str>
    return data_formated


@dp.message_handler(commands="start")  # Приветственное сообщение
async def start(message: types.Message):
    if not BotDB.user_exists(
        message.from_user.id
    ):  # Проверям наличие пользователя в БД
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(
        message.from_user.id,
        "Добро пожаловать! Я твой личный бухгалтер 😊. Я буду запоминать все твои "
        "расходы и доходы.",
    )


# Вывод сообщение при команде /help
@dp.message_handler(commands="help")  # Приветственное сообщение
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    await message.bot.send_message(
        message.from_user.id,
        f"Мои команды:\n /spent, /s, !spent, !s - запоминают расход\n /earned, /e, !earned, "
        f"!e - запоминают доход \n /history, /h, !history, !h - выдают отчет расходов"
        f" \n !h месяц - за месяц\n !h год - за год",
    )


@dp.message_handler(
    commands=("spent", "earned", "s", "e"), commands_prefix="/!"
)  # Ловим сообщение с префиксом "/!" и операцией доход/расход
async def start(message: types.Message):
    cmd_variants = (
        ("/spent", "/s", "!spent", "!s"),
        ("/earned", "/e", "!earned", "!e"),
    )
    operation = (
        "-" if message.text.startswith(cmd_variants[0]) else "+"
    )  # записываем в переменную доход или расход
    value = message.text
    info, group = "", ""
    for i in cmd_variants:  # Узнаем тип операции
        for j in i:
            value = value.replace(j, "").strip()
    inf = value
    # цикл выделение всей текстовой части после ввода суммы
    for i in range(len(inf)):
        if inf[i] in " ":
            info = inf[i + 1 :]

            break

    if len(value):
        x = re.findall(
            r"\d+(?:.\d+)?", value
        )  # выделяем числовое значение из всего текста
        if len(x):
            value = float(x[0].replace(",", "."))
            BotDB.add_record_1(
                message.from_user.id, operation, value, info, group
            )

            if operation == "-":
                await message.reply(
                    "✔ Запись о <u><b>расходе</b></u> успешно внесена!",
                    reply=False,
                )
            else:
                await message.reply(
                    "✔ Запись о <u><b>доходе</b></u> успешно внесена!",
                    reply=False,
                )
        else:
            await message.reply("Не удалось определить сумму!", reply=False)
    else:
        await message.reply("Не введена сумма!", reply=False)


@dp.message_handler(
    commands=("history", "h"), commands_prefix="/!"
)  # Ловим команда для выдачи отчета о расходах за день/месяц/год
async def start(message: types.Message):
    cmd_variants = ("/history", "/h", "!history", "!h")
    within_als = {
        "day": ("today", "day", "сегодня", "день"),
        "month": ("month", "месяц"),
        "year": ("year", "год"),
    }

    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, "").strip()

    within = "day"  # значение отчета по умолчанию
    if len(cmd):
        for k in within_als:
            for als in within_als[k]:
                if als == cmd:
                    within = k

    records = BotDB.get_records(message.from_user.id, within)

    if len(records):
        answer = f"🕘 История операций за {within_als[within][-1]}\n\n"

        for r in records:
            answer += (
                "<b>" + ("➖ Расход" if not r[2] else "➕ Доход") + "</b>"
            )  # расход или доход
            answer += f" - {r[3]}"  # Cумма
            answer += f" <i>({data_format(r[4])})</i>"  # Дата
            answer += f" {r[5]}\n"  # Инфо
        await message.reply(answer, reply=False)
    else:
        await message.reply("Записей не обнаружено!", reply=False)


# @dp.message_handler(commands=("statistic", "статистика"),
#                     commands_prefix="/!"
#                     )
# async def handler_statistic(message: types.Message):
#     answer = statistic.get_statistic(message.text, message.from_user.id)
#     await message.reply(answer, reply=False)


@dp.message_handler(commands=("courses", "курсы", "c"), commands_prefix="/!")
async def start(message: types.Message):
    cmd_variants = ("/n", "!n")
    within_als = {
        "parse_bsb": ("bsb", "бсб"),
        "parse_alfa": ("alfa", "альфа"),
        "parse_belweb": ("belweb", "белвэб"),
        "parse_prior": ("prior", "приор"),
    }
    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, "").strip()  # удаляем команду из текста
    within = "parse_all"
    if len(cmd):
        for k in within_als:
            for als in within_als[k]:
                if als == cmd:
                    within = k
    result = eval(within)()
    await message.reply(result, reply=False)


#     operation = '-' if message.text.startswith(cmd_variants[0]) else '+' #записываем в переменную доход или расход
#     value = message.text
#     info = ''
#
#     for i in cmd_variants:            #Узнаем тип операции
#         for j in i:
#             value = value.replace(j, '').strip() #отбрасываем команду расхода/дохода
#     inf = value
#     # цикл выделение всей текстовой части после ввода суммы
#     for i in range(len(inf)):
#         if inf[i] in ' ':
#             info = inf[i+1:]
#             break
#
#
#     if(len(value)):
#         x = re.findall(r"\d+(?:.\d+)?", value) #выделяем числовое значение из всего текста
#
#         if(len(x)):
#             value = float(x[0].replace(',', '.'))  #в переменной value записана только сумма
#
#             BotDB.add_record_1(message.from_user.id, operation, value, info)
#
#             if(operation == '-'):
#                 await message.reply("✔ Запись о <u><b>расходе</b></u> успешно внесена!")
#             else:
#                 await message.reply("✔ Запись о <u><b>доходе</b></u> успешно внесена!")
#         else:
#             await message.reply("Не удалось определить сумму!")
#     else:
#         await message.reply("Не введена сумма!")
