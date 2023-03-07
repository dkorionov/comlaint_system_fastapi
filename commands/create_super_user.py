import asyncclick as click

from managers.user import UserManager
from models import RoleType
from db import database


@click.command()
@click.option('-f', '--first-name', type=str, required=True, help='First name')
@click.option('-l', '--last-name', type=str, required=True, help='last name')
@click.option('-e', '--email', type=str, required=True, help='Email')
@click.option('-p', '--phone', type=str, required=True, help='Phone')
@click.option('-i', '--iban', type=str, required=True, help='IBAN')
@click.option('-pa', '--password', type=str, required=True, help='Password')
async def create_user(first_name: str, last_name: str, email: str, iban: str, password: str, phone: str):
    user_data = {'first_name': first_name, 'last_name': last_name, 'email': email,
                 "phone": phone, 'iban': iban, 'password': password, "role": RoleType.ADMIN}
    await database.connect()
    await UserManager.register(user_data)
    await database.connect()


if __name__ == '__main__':
    create_user(_anyio_backend='asyncio')
