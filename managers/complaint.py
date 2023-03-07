import os.path
import uuid

from constants import MEDIA_DIR
from db import database
from models import transaction_model
from models.complaint import complaint_model, State
from models.user import RoleType
from services.s3_service import S3Service
from services.utils import decode_image
from services.wise_service import WiseService

s3 = S3Service()
wise = WiseService()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user: dict):
        q = complaint_model.select()
        if user['role'] == RoleType.COMPLAINER:
            q = q.where(complaint_model.c.complainer_id == user['id'])
        elif user['role'] == RoleType.APPROVER:
            q = q.where(complaint_model.c.state == State.PENDING)
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint: dict, user: dict):
        complaint['complainer_id'] = user['id']
        encoded_image = complaint.pop("encoded_image")
        extension = complaint.pop("extension")
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(MEDIA_DIR, name)
        decode_image(path, encoded_image)
        complaint['photo_url'] = s3.upload_image(path, name, extension)
        os.remove(path)
        async with database.transaction() as tcon:
            id_ = await tcon._connection.execute(complaint_model.insert().values(**complaint))
            await ComplaintManager.create_transaction(tcon, complaint['amount'],
                                                      f"{user['first_name']} {user['last_name']}",
                                                      user['iban'], id_)
        return await database.fetch_one(complaint_model.select().where(complaint_model.c.id == id_))

    @staticmethod
    async def delete(id_: int):
        await database.execute(complaint_model.delete().where(complaint_model.c.id == id_))

    @staticmethod
    async def approve(id_: int):
        await database.execute(complaint_model.update().where(complaint_model.c.id == id_).values(state=State.APPROVED))
        transaction_data = database.fetch_one(transaction_model.select().where(transaction_model.c.complaint_id == id_))
        wise.fund_transfer(transaction_data['transfer_id'])

    @staticmethod
    async def reject(id_: int):
        transaction_data = database.fetch_one(transaction_model.select().where(transaction_model.c.complaint_id == id_))
        wise.cancel_fund_transfer(transaction_data['id'])
        await database.execute(complaint_model.update().where(complaint_model.c.id == id_).values(state=State.REJECTED))

    @staticmethod
    async def create_transaction(tconn, amount: float, full_name: str, iban: str, complaint_id: int):
        quote_id = wise.create_quote(amount)
        recipient_id = wise.create_recipient_account(full_name, iban)
        transfer_id = wise.create_transfer(recipient_id, quote_id)
        data = {
            "quote_id": quote_id,
            "transfer_id": transfer_id,
            "target_account_id": str(recipient_id),
            "amount": amount,
            "complaint_id": complaint_id,
        }
        await tconn._connection.execute(transaction_model.insert().values(**data))
