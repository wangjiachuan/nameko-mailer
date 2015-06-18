import mandrill
from nameko.extensions import DependencyProvider


API_KEY = "8eZMbUkC5HFrN79k1JwHBg"


class ApiWrapper(object):

    def __init__(self, session):
        self.session = session

    def send_message(self, payload):
        return self.session.messages.send(message=payload)


class MandrillService(DependencyProvider):

    def setup(self):
        self.session = mandrill.Mandrill(API_KEY)

    def get_dependency(self, worker_ctx):
        return ApiWrapper(self.session)