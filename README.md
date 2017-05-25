# Drchrono Wish Your patient app
A web application that lets users login using their drchrono account and send birthday wishes to their patients.

### Requirements
- [pip](https://pip.pypa.io/en/stable/)
- [python virtual env](https://packaging.python.org/installing/#creating-and-using-virtual-environments)

### Setup
``` bash
$ pip install -r requirements.txt
$ python manage.py migrate
```

`social_auth_drchrono/` contains a custom provider for [Python Social Auth](http://psa.matiasaguirre.net/) that handles OAUTH for drchrono. To configure it, set these fields in your `drchrono/settings.py` file:

```
SOCIAL_AUTH_DRCHRONO_KEY
SOCIAL_AUTH_DRCHRONO_SECRET
LOGIN_REDIRECT_URL
```

In addition to the above settings, the email settings need to be configured in the `drchrono/settings.py` file:

```
EMAIL_HOST
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
EMAIL_PORT
DEFAULT_FROM_EMAIL
```

Server can be started using:

``` bash
$ python manage.py runserver
```

### About the application
###### Three ways to send emails
- 'Send wishes to all' allows the user to send emails to all the patients who have birthdays today instead of sending to individual patients. A message preview indicates that the patient name will be prepended to the message before sending.
- 'Quick send' allows the user to compose a message and send it quickly to a single patient without going into much details.
- The 'View' button expands a panel with the details of the selected patient such as photo, gender etc. and includes a text area to compose and send an email from the details panel.
###### Features
- Birthdays are displayed based on the client timezone.
- A default message is provided in the text area so that the user has click-to-send option.
- If a patient does not have an email address on file, the text area is disabled and send button is hidden and an appropriate message is shown to the user.
- Cancel button to hide panel shown by any of the above three sending modes.
- Send and cancel buttons disabled when email sending is in progress in order to avoid erratic behaviour.
- Only one sending mode panel displayed at any time. Opening one closes the other.
- Appropriate feedback displayed to the user for every action taken.
- Refreshing the page fetches new birthdays if the client date changes during the same session.
- Responsive design.