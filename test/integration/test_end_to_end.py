import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from service.test_service import PaymentService
from mailer.service import Mailer
from nameko.runners import ServiceRunner


config = {'AMQP_URI': 'amqp://guest:guest@localhost:5672/'}
runner = ServiceRunner(config)

# Add Mailer service. Dependant Payment Service will be started automatically.
runner.add_service(Mailer)

runner.start()

