import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../../")

from mailer.service import Mailer
from nameko.testing.services import worker_factory
from faker import Factory

fake = Factory.create()


class TestMailer:
    def test_will_send_valid_payload(self):
        test_service = worker_factory(Mailer)
        assert test_service.handle_event(self.valid_payload())["success"]

    def test_will_not_send_invalid_payload(self):
        test_service = worker_factory(Mailer)
        results = test_service.handle_event(self.invalid_payload())
        assert results["success"] == False
        assert len(results["errors"]) == 1
        assert results["errors"][0] == "Invalid Payload"


    @staticmethod
    def valid_payload():
        return {
            "client": {
                "name": fake.name(),
                "email": fake.safe_email()
            },
            "payee": {
                "name": fake.name(),
                "email": fake.safe_email()
            },
            "payment": {
                "amount": fake.random_int(),
                "currency": fake.random_element(
                    ("USD", "GBP", "EUR")
                )
            }
        }

    def invalid_payload(self):
        payload = self.valid_payload()
        payload["payment"]["amount"] = "invalid"
        return payload