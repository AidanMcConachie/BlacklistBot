# Blacklists Bot

This uses an older version of the **Discord API** to ban users before joining the server, using a *shared* database.

Users with ban permissions can add user IDs to databases for their server.

When a user joins a server with Blacklists, it checks if their discord id is in the database for their guild. If it is, it permanently bans them instantly.

