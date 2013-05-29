pyGeoBot
========

**pyGeoBot** - an IRC bot in python.

Main features
--------------

* Link recognition
  - Grabbing link titles
  - Grabbing some info if it's [YouTube](http://www.youtube.com) link
  - Grabbing [Twitter](http://www.twitter.com)'s status links
* This yet.

Configuration
-------------

If in any case you want to change configuration of bot you must change **config.json**, or you can change source code of **main.py**. 
For quick configuring 
- fill fields in `empty_config.json`
- rename it to `config.json`
- and run 

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
- `auth` - message that bot will send when it will connect and join all channels (i.e. `PRIVMSG NickServ :IDENTIFY bleh`)
- `twitter` - type of **JSONObject**, should contain `consumer` object, which must contain `key` and `secret`. Perhaps you need to register application on [Twitter](https://dev.twitter.com/apps) to make bot's twitter module work. Or there you can add `access_token` field instead of `consumer`, and fill there Twitter's access token, that will work also.
- `password` - password for controlling bot over **IRC**
- `autojoin_on_kick` - true or false, join to channel when was kicked from it ?

Starting bot
------------
To start bot
- make sure you have watched and did steps of configuration ([here](https://github.com/geohhot/PyGeoBot#configuration-keys))
- Choose if you want to see its output, or you just want it to start in new process and let it live there (i.e. if you're about to host bot somewhere) do `./start.sh`, and whenever you will want to stop it do `./stop.sh` 
- Or if you want to see bot's *pretty* output, just do `python src/main.py` (from repo's root directory)

LICENSE
-------
This bot is under [MIT](https://github.com/geohhot/PyGeoBot/blob/master/LICENSE) license. Read more about it [here](http://en.wikipedia.org/wiki/MIT_License)

Thanks to
---------

My "friends" for finding bugs through making **stupid** jokes on me and [blandflakes](blandflakes) for contributing.