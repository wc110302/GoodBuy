import random

from app.models import UserTicket


def get_ticket():
    s = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
    ticket = ''
    for i in range(30):
        ticket += random.choice(s)
    ticket = 'TK_' + ticket
    return ticket


def get_user(request):
    ticket = request.COOKIES.get('ticket')
    user_ticket = UserTicket.objects.filter(ticket=ticket).first()
    user = user_ticket.user
    return user