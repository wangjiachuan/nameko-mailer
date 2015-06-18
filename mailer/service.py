from nameko.events import event_handler
import mandrill
from jsonschema import validate, exceptions


class Mailer(object):
    """ This is a main service class accepting messages payloads from payments service.

        TODO:
        - Remove hard dependency on Mandrill and allow for swapping for different implementations.
            Potentially use concept of Nameko Dependencies.
        - Move Madrill API Key to environment variable
    """
    name = "mailer"

    mailer_provider = mandrill.Mandrill("8eZMbUkC5HFrN79k1JwHBg")


    @event_handler("payments", "payment_received")
    def handle_event(self, payload):

        """
        Args:
            payload (object): all necessary data for sending email client
        """

        print "Payload received", payload

        results = {
            "success": False,
            "errors": []
        }

        if not validate_payload(payload):
            results["success"] = False
            results["errors"].append("Invalid Payload")
            return results

        try:
            message_text = construct_message_text(payload)
            message = construct_message(message_text, payload)
            self.mailer_provider.messages.send(message=message)

            results["success"] = True
            return results

        except mandrill.Error, e:
            results["success"] = False
            results["errors"].append("A mandrill error occurred: %s - %s" % (e.__class__, e))


def validate_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "client": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                }
            },
            "payee": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                }
            },
            "payment": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "currency": {"type": "string"},
                }
            },
        },
    }

    try:
        validate(payload, schema)
        return True
    except exceptions.ValidationError, e:
        return False


def construct_message_text(payload):
    return "Dear {0}, \n\nYou have received a payment of {1} {2} from {3} ({4}). \n\nYours, student.com" \
        .format(payload.get("payee")["name"],
                payload.get("payment")["amount"],
                payload.get("payment")["currency"],
                payload.get("client")["name"],
                payload.get("client")["email"])


def construct_message(message_text, payload):
    return {
        # TODO: User env variable for from email.
        "from_email": "jakub.borys@gmail.com",
        "from_name": "Team at Student.com",
        "text": message_text,
        "to": [{"email": payload.get("payee")["email"],
                "name": payload.get("payee")["name"],
                "type": "to"}],
    }