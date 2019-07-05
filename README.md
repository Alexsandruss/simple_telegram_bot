### Just simple telegram bot

#### Features:
- bot responses on "/" and "?" commands that are specified in the file "commands.json" (answers also there);
- shows random quote on "/quote" command (quotes are stored in "quotes.json");
- throws N-edged dice M times on "/dice N-edged M times" command;
- randomly chooses variant on "/random 1st_variant 2nd_variant 3rd_variant etc";
- shows days until New Year and summer on "/newyear" and "/summer" commands;
- gives location with coordinates on "/where <location>" command;
- shows the location on map by coordinates on "/location <latitude> <longitude>" command;
- shows telegram chat id on "/chat_id" command;
- shows seconds since 00:00:00 1 January 1970 on "/unix_time" command;
- shows what holiday is today on "/holiday" command;
- shows color specified in RGB format on "/rgb <Red> <Green> <Blue>" command;
- opens lootbox on "/lootbox" command.

#### Installation:
- copy repository;
- create bot and get token from BotFather(https://t.me/BotFather);
- insert token in db.json;
- run main.py.
