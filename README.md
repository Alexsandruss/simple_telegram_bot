Just simple telegram bot

Features:
1. bot responses on "/" and "?" commands that are specified in the file "commands.json" (answers also there);
2. shows random quote on "/quote" command (quotes are stored in "quotes.json");
3. shows bitcoin/ethereum/ripple rates (update every 10 minutes) on "/bitcoin", "/ethereum" or "/ripple" commands;
4. throws N-edged dice M times on "/dice N-edged M times" command;
5. randomly chooses variant on "/random 1st_variant 2nd_variant 3rd_variant etc";
6. shows days until New Year and summer on "/newyear" and "/summer" commands;
7. gives location with coordinates on "/where <location>" command;
8. shows shows telegram chat id on "/chat_id" command.

Installation:
1. copy repository;
2. create bot and get token from BotFather(t.me/BotFather);
3. insert token in db.json;
4. run main.py.