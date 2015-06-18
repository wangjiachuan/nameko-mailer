from nameko.events import event_handler
import mandrill


class Mailer(object):
    name = "mailer"


    @event_handler("payments", "payment_received")
    def handle_event(self, payload):

        # print "service b received", payload
        print "client", payload.get('client')['name']

        mailer_provider = mandrill.Mandrill("8eZMbUkC5HFrN79k1JwHBg")

        message_text = "Dear {0}, \n\nYou have received a payment of {1} {2} from {3} ({4}). \n\nYours, student.com" \
            .format(payload.get('payee')['name'],
                    payload.get('payment')['amount'],
                    payload.get('payment')['currency'],
                    payload.get('client')['name'],
                    payload.get('client')['email'])

        try:
            message = {
                # TODO: User env variable for from email.
                'from_email': 'jakub.borys@gmail.com',
                'from_name': 'Team at Student.com',
                'text': message_text,
                'to': [{'email': payload.get('payee')['email'],
                        'name': payload.get('payee')['name'],
                        'type': 'to'}],
            }

            result = mailer_provider.messages.send(message=message)

            print result
            return 'success'

        except mandrill.Error, e:
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            raise
