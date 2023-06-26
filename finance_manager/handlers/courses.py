import orjson as orjson
import requests
from bs4 import BeautifulSoup as bs


def parse_bsb() -> str:
    url_bsb = """https://bsb.by/"""
    response_text = requests.get(url_bsb).text
    soup = bs(response_text, "html.parser")
    html_data = soup.find_all("div", class_="currency-tab")

    exchange = soup.find_all("span", class_="exchange-scale")
    names = [name.text for name in exchange]  # cписок валют
    value_data = soup.find_all("td")
    value = [value.text for value in value_data][:6]

    result_data = (
        f"Курсы валют в БСБ банке\n"
        f"        покупка   продажа\n"
        f"1   {names[0]} {value[0]}    {value[1]}\n"
        f"1   {names[1]} {value[2]}    {value[3]}\n"
        f"100 {names[2]} {value[4]}    {value[5]}\n"
    )

    return result_data


def parse_alfa() -> str:
    url_alfa = "https://www.alfabank.by/exchange/minsk/"
    response_text = requests.get(
        url_alfa,
        headers={
            "sec-ch-ua": "Opera",
            "sec-ch-ua-platform": "Windows",
            "User-Agent": "Mozilla/5.0",
        },
    ).text
    soup = bs(response_text, "html.parser")
    html_data = soup.find(attrs={"data-component": "ExchangePage"})
    str_data = str(html_data)[49:-9]
    py_data = orjson.loads(str_data)
    initial_items = py_data["initialItems"]
    for item in initial_items:
        if item.get("id") == "617955":  # alfabank corparate
            corporate_minsk = item
    courses_data = (
        corporate_minsk.get("currenciesData")[0]
        .get("value")
        .get("exchangeRate")
    )
    course_usd = courses_data[0]
    course_eur = courses_data[1]
    course_rub = courses_data[2]
    result_data = (
        f"Курсы валют в Альфа банке\n"
        f"Отделение {corporate_minsk.get('title')}\n"
        f"{course_usd.get('title')} покупка {course_usd.get('purchase').get('value')} "
        f"продажа {course_usd.get('sell').get('value')}\n"
        f"{course_eur.get('title')} покупка {course_eur.get('purchase').get('value')} "
        f"продажа {course_eur.get('sell').get('value')}\n"
        f"{course_rub.get('title')} покупка {course_rub.get('purchase').get('value')} "
        f"продажа {course_rub.get('sell').get('value')}\n"
    )
    return result_data


def parse_belweb() -> str:
    url_belweb = "https://www.belveb.by/rates/"
    response_text = requests.get(url_belweb).text
    soup = bs(response_text, "html.parser")
    html_data = soup.find(name="v-currency-other")
    courses_str = str(html_data)[32:-21]
    py_data = orjson.loads(courses_str)
    courses_data = py_data.get("items")[0].get("currency")
    courses_address = py_data.get("items")[0].get("address")
    courses_usd = courses_data[0]
    courses_eur = courses_data[1]
    courses_rub = courses_data[2]
    result_data = (
        f"Курсы валют в БелВЭБ банке\n"
        f"{courses_address}\n"
        f"{courses_usd.get('currency_qty')} {courses_usd.get('currency_cod')} "
        f"покупка {courses_usd.get('buy_rate').get('value')} "
        f"продажа {courses_usd.get('sale_rate').get('value')}\n"
        f"{courses_eur.get('currency_qty')} {courses_eur.get('currency_cod')} "
        f"покупка {courses_eur.get('buy_rate').get('value')} "
        f"продажа {courses_eur.get('sale_rate').get('value')}\n"
        f"{courses_rub.get('currency_qty')} {courses_rub.get('currency_cod')} "
        f"покупка {courses_rub.get('buy_rate').get('value')} "
        f"продажа {courses_rub.get('sale_rate').get('value')}\n"
    )
    return result_data


def parse_prior() -> str:
    # url_prior= "https://priorbank.by"
    # response_text = requests.get(url_prior, headers={'sec-ch-ua': 'Opera', 'sec-ch-ua-platform': 'Windows',
    #                                               'User-Agent': "Mozilla/5.0"}).text
    # html_data_buy_rate = soup.find('div', class_='homeModuleColumn homeModuleColumn--2')
    url_prior_post = (
        "https://www.priorbank.by:443/main?p_p_id=ExchangeRates_INSTANCE_"
        "OmGEhZK5B4W2&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_"
        "id=ajaxMainPageRatesGetRates&p_p_cacheability=cacheLevelPage"
    )
    response = requests.post(url_prior_post)
    response_text = response.json().get("resultCard")
    soup = bs(response_text, "html.parser")
    html_data = soup.find_all("span", class_="value")
    courses_data = [item.text for item in html_data]
    courses_name = courses_data[1:4]
    courses_buy_rate = courses_data[4:8]
    courses_sell_rate = courses_data[8:12]
    result_data = (
        f"Курсы валют в Приорбанк\n"
        f"1 {courses_name[0]} {courses_buy_rate[0]} {courses_buy_rate[1]} {courses_sell_rate[0]} {courses_sell_rate[1]}\n"
        f"1 {courses_name[1]} {courses_buy_rate[0]} {courses_buy_rate[2]} {courses_sell_rate[0]} {courses_sell_rate[2]}\n"
        f"{courses_name[2][7:]} {courses_buy_rate[0]} {courses_buy_rate[2]} {courses_sell_rate[0]} {courses_sell_rate[2]}\n"
    )
    return result_data


def parse_all() -> str:
    result = (
        parse_bsb()
        + "\n"
        + parse_belweb()
        + "\n"
        + parse_prior()
        + "\n"
        + parse_alfa()
    )
    return result
