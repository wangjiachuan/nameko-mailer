import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from mailer.service import Mailer
from nameko.testing.services import worker_factory
from faker import Factory

fake = Factory.create()


class TestMailer:
    def test_mailier_service(self):
        payload = {
            'client': {
                'name': fake.name(),
                'email': fake.safe_email()
            },
            'payee': {
                'name': fake.name(),
                'email': fake.safe_email()
            },
            'payment': {
                'amount': fake.random_int(),
                'currency': fake.random_element(
                    ("USD", "GBP", "EUR")
                )
            }
        }

        test_service = worker_factory(Mailer)
        assert test_service.handle_event(payload) == 'success'