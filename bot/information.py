import discord.ext.commands as cmd
from database.database import get_country_name
import requests


class Information(cmd.Cog):
    url = 'https://api.covid19api.com/'

    def __init__(self, bot):
        self.bot = bot

    @cmd.command()
    async def covid(self, ctx: cmd.Context, country=None):
        if not country:
            res = self.global_covid_info()
        else:
            res = self.country_info(country)
        await ctx.send(res)

    def global_covid_info(self):
        response = requests.get(self.url + 'summary')
        data = response.json()['Global']
        return f"""Глобальная статистика по распространению COVID-19 на {response.json()['Date']}
Новых случаев: {data['NewConfirmed']:,}
Всего зафиксировано случаев: {data['TotalConfirmed']:,}
Новых летальных случаев: {data['NewDeaths']:,}
Всего летальных случаев: {data['TotalDeaths']:,}
Вылечевшихся: {data['NewRecovered']:,}
Всего вылечилось: {data['TotalRecovered']:,}"""

    def country_info(self, country):
        if len(country) == 2:
            country = get_country_name(country.upper())
            if not country:
                return 'Не могу найти страну с таким кодом.'
        response = requests.get(f'{self.url}/total/country/{country}')
        if len(response.json()) == 0:
            return 'Не могу найти такую страну.'
        data = response.json()[-1]
        return f"""Статистика по распространению COVID-19 в {country.capitalize()} на {data['Date'][:10]}
Зафиксированных случаев: {data['Confirmed']:,}
Летальных случаев: {data['Deaths']:,}
Выздровевших: {data['Recovered']:,}"""
