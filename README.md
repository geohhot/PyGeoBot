pyGeoBot
========

**pyGeoBot** - an IRC bot in python.

Main features
--------------

* Link recognition
  - Grabbing link titles
  - Grabbing some info if it's [YouTube](http://www.youtube.com) link
  - Grabbing Twitter link (work is in progress)
* This yet.

Configuring
-----------

If in any case you want to change configuration of bot you must change **config.json**, or you can change source code of **main.py**

### Configuration keys
- `ircServerHost` - **IP** or **hostname** of *IRC Server*
- `ircServerPort` - *port* of *IRC Server* (6667 by default)
- `ircServerPassword` - **password** of *IRC Server* (if password is set on it)
- `nicname` - *nickname* of bot
- `realname` - **IRC** field for *realname* (by default: `Py Geo Bot (http://bit.ly/12S9zlD)`)
- `username` - **IRC** username
- `debug` - boolean of debug output or no
- `channels` - JSON array, contains channels that bot must join
- `log` - specifies log file's name
- `auth` - message that bot will send when it will connect and join all channels (i.e. `PRIVMSG NickServ IDENTIFY bleh`)

Thanks to
---------

My "friends" for finding bugs through making **stupid** jokes on me and [blandflakes](blandflakes) for contributing,