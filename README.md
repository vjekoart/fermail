# fermail
Simple command-line tool to check unread messages on webmail@fer service written in Python2.7.

## Usage

Edit config.ini file with your login data, then run in command-line to get list of unread mails:
```
python2.7 mailer.py
```

You can also use arguments **help** and **check** to see list of all arguments and to check config file.

Password is stored in base64 inside config.ini file.
