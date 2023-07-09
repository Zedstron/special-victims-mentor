from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.conf import settings
from datetime import datetime

def Parse(strdate):
    dt = datetime.strptime(strdate, "%m/%d/%Y")
    return str(dt.isoformat('T'))

def CreateEvent(request, title, description, start, end, institution, deadline, instructions, calendar='primary'):
    user = SocialAccount.objects.get(user=request.user)
    token = SocialToken.objects.get(account=user).token
    creds = Credentials(token, settings.GOOGLE_CALENDAR_SCOPES )

    service = build(
        settings.GOOGLE_CALENDAR_API_NAME,
        settings.GOOGLE_CALENDAR_API_VERSION,
        credentials=creds,
    )

    description = f'''
        DESCRIPTION
        {description}

        INSTITUTION
        {institution}

        INSTRUCTIONS
        {instructions}
        
        DEADLINE
        {deadline}'''

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': Parse(start),
            'timeZone': 'Asia/Karachi',
        },
        'end': {
            'dateTime': Parse(end),
            'timeZone': 'Asia/Karachi',
        },
        'attendees': [ request.user.email ],
        'reminders': {
            'useDefault': True,
        }
    }

    event = service.events().insert(calendarId=calendar, body=event).execute()
    return event.get('id')
