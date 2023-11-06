# from viberbot import Api
# from viberbot.api.bot_configuration import BotConfiguration
#
# bot_configuration = BotConfiguration(
# 	name='I-CONT_Viber_Chat_Bot',
# 	avatar='https://viber.com/avatar.jpg',
# 	auth_token='51e5e12627e7dcce-1078089ef2cdfee5-9a2492f6e91dd198'
# )
# viber = Api(bot_configuration)


from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest

from viberbot.api.messages import (
    TextMessage,
    ContactMessage,
    PictureMessage,
    VideoMessage
)
from viberbot.api.messages.data_types.contact import Contact

# creation of text message
text_message = TextMessage(text="Teszt üzenet!")

contact = Contact(name="Fannikám", phone_number="+36702516775")
contact_message = ContactMessage(contact=contact)


app = Flask(__name__)
viber = Api(BotConfiguration(
    name='I-CONT_Viber_Chat_Bot',
    avatar='https://viber.com/avatar.jpg',
    auth_token='51e5e12627e7dcce-1078089ef2cdfee5-9a2492f6e91dd198'
))


@app.route('/', methods=['POST'])
def incoming():
	viber_request = viber.parse_request(request.get_data())

	if isinstance(viber_request, ViberConversationStartedRequest) :
		viber.send_messages(viber_request.get_user().get_id(), [
			TextMessage(text="Welcome!")
		])

	return Response(status=200)

"""app = Flask(__name__)
viber = Api(BotConfiguration(
    name='I-CONT_Viber_Chat_Bot',
    avatar='https://viber.com/avatar.jpg',
    auth_token='51e5e12627e7dcce-1078089ef2cdfee5-9a2492f6e91dd198'
))

@app.route('/', methods=['POST'])
def incoming():
    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        # lets echo back
        viber.send_messagaes(viber_request.sender.id, [
            TextMessage(text="Your id is: " + str(viber_request.sender.id))
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="Change The Way You Look At Things And The Things You Look At Change!")
        ])

    return Response(status=200)

if __name__ == "__main__":
    app.run(port=5001)
    #app.run(host='https://viberboturl.pythonanywhere.com', port=443, debug=True)"""