from nameko.events import event_handler


class Mailer(object):

    name = "mailer"

    @event_handler("payments", "payment_received")
    def handle_event(self, payload):
        print "service b received", payload