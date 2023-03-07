import json
import uuid
from decouple import config
import requests
from fastapi import HTTPException, status


class WiseService:
    def __init__(self) -> None:
        self.main_url = config('WISE_URL')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}",
        }

        self.profile_id = self._get_profile_id()

    def _get_profile_id(self) -> int:
        url = f"{self.main_url}/v2/profiles"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return [el["id"] for el in response.json() if el['type'] == "personal"][0]
        else:
            # log the exception
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Pyment provider is not available at the moment")

    def create_quote(self, amount: float) -> str:
        url = f"{self.main_url}/v2/quotes"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": amount,
            "profile": self.profile_id
        }
        response = requests.post(url, headers=self.headers, json=json.dumps(data))
        if response.status_code == 200:
            return response.json()['id']
        else:
            # log the exception
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Pyment provider is not available at the moment")

    def create_recipient_account(self, full_name: str, iban: str) -> str:
        url = self.main_url + "/v1/accounts"
        data = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "ownedByCustomer": True,
            "accountHolderName": full_name,
            "details": {
                "legalType": "PRIVATE",
                "iban": iban,
            }
        }
        response = requests.post(url, headers=self.headers, json=json.dumps(data))
        if response.status_code == 200:
            return response.json()['id']
        else:
            # log the exception
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Pyment provider is not available at the moment")

    def create_transfer(self, target_account_id: str, quote_id: str) -> int:
        url = self.main_url + "/v1/transfers"
        customer_transaction_id = str(uuid.uuid4())
        data = {
            "TargetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
        }
        response = requests.post(url, headers=self.headers, json=json.dumps(data))
        if response.status_code == 200:
            return response.json()['id']
        else:
            # log the exception
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Pyment provider is not available at the moment")

    def fund_transfer(self, target_id: int):
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/transfers/{target_id}/payments"
        data = {
            "type": "BALANCE",
        }
        response = requests.post(url, headers=self.headers, json=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            # log the exception
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Pyment provider is not available at the moment")

    def cancel_fund_transfer(self, transfer_id: int):
        url = self.main_url + f"/v1/transfers/{transfer_id}/cancel"
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            # log the exception
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Pyment provider is not available at the moment")
