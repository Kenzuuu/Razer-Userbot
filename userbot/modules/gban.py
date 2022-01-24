from telethon.events import ChatAction
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import MessageEntityMentionName

from userbot import ALIVE_NAME, CMD_HELP, DEVS, bot
from userbot.events import register


async def get_full_user(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit(
                             f"**⚠️ Warning . . !** /n/n"
                             f"👷`User ID required!`"
                            )
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(
                    probable_user_mention_entity,
                    MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit(
                "**⚠️ Warning . . !**\n\n`Errors Found, Report to :` **[MASTER](https://t.me/triplenineee)** ", str(err)
            )
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


@bot.on(ChatAction)
async def handler(tele):
    if tele.user_joined or tele.user_added:
        try:
            from userbot.modules.sql_helper.gmute_sql import is_gmuted

            guser = await tele.get_user()
            gmuted = is_gmuted(guser.id)
        except BaseException:
            return
        if gmuted:
            for i in gmuted:
                if i.sender == str(guser.id):
                    chat = await tele.get_chat()
                    admin = chat.admin_rights
                    creator = chat.creator
                    if admin or creator:
                        try:
                            await client.edit_permissions(
                                tele.chat_id, guser.id, view_messages=False
                            )
                            await tele.reply(
                                f"**🚫 BANNED USER :** \n\n"
                                f"**👷 User**: [{guser.id}](tg://user?id={guser.id})\n"
                                f"**⚙️ Action**  : `Banned` ✅"
                            )
                        except BaseException:
                            return


@register(outgoing=True, pattern="^.gban(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^\.cgban(?: |$)(.*)")
async def gben(userbot):
    dc = userbot
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if not sender.id == me.id:
        dark = await dc.reply(
                              f"**🚫 GLOBAL BAN** \n\n "
                              f"⚙️ Starting Action . . !")
    else:
        dark = await dc.edit(
                             f"**🚫 GLOBAL BAN** \n\n "
                             f"`⚙️ Waiting Process. . !`")
    me = await userbot.client.get_me()
    await dark.edit(
                    f"**🚫 GLOBAL BAN** \n\n "
                    f"`⚙️ Processing Gban . . !`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await dark.edit(f"`❌ Stopping Process`")
    if user:
        if user.id in DEVS:
            return await dark.edit(
                f"`❌ Stoping process, He is my` **[Master](https://t.me/triplenineee)** "
            )
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except BaseException:
            pass
        try:
            await userbot.client(BlockRequest(user))
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, view_messages=False)
                a += 1
                await dark.edit(
                                f"**🚫 GLOBAL BAN** \n\n "
                                f"⚙️ `Process activated By :` **[MASTER](https://t.me/triplenineee)**")
            except BaseException:
                b += 1
    else:
        await dark.edit(
                        f"**🚫 GLOBAL BAN** \n\n "
                        f"📩`Reply message required`")
    try:
        if gmute(user.id) is False:
            return await dark.edit(
                f"❌`This user has been banned `"
            )
    except BaseException:
        pass
    return await dark.edit(
        f"**🚫 GLOBAL BAN**\n\n🤴 **Request:** `{ALIVE_NAME}`\n👷 **User:** [{user.first_name}](tg://user?id={user.id})\n⚙️ **Action :** `Global Banned!` ✅"
    )


@register(outgoing=True, pattern="^.ungban(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^\.cungban(?: |$)(.*)")
async def gunben(userbot):
    dc = userbot
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if not sender.id == me.id:
        dark = await dc.reply(
                              f"**🚫 UNGLOBAL BAN** \n\n "
                              f"⚙️ `Starting Action . . !`")
    else:
        dark = await dc.edit(
                             f"**🚫 UNGLOBAL BAN** \n\n "
                              f"⚙️ `Waiting Action . . !`")
    me = await userbot.client.get_me()
    await dark.edit(
        f"`🔐 Starting Process Unban`"
    )
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await dark.edit("❌ `Stopping Process`")
    if user:
        if user.id in DEVS:
            return await dark.edit(
                "❌ `Stopping process, He is my` **[Master](https://t.me/triplenineee)**"
            )
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except BaseException:
            pass
        try:
            await userbot.client(UnblockRequest(user))
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await dark.edit(
                                f"**🚫 UNGLOBAL BAN** \n\n "
                                f"⚙️ `Process Ungban User `")
            except BaseException:
                b += 1
    else:
        await dark.edit(
                        f"**🚫 GLOBAL BAN** \n\n "
                        f"`📩 Reply message Required`")
    try:
        if ungmute(user.id) is False:
            return await dark.edit(
                "❌ Users are not in the black list "
            )
    except BaseException:
        pass
    return await dark.edit(
        f"🤴 **Request By :** `{ALIVE_NAME}`\n👷 **For User:** [{user.first_name}](tg://user?id={user.id})\n⚙️ **Action:**`Ungban User` ✅"
    )


CMD_HELP.update(
    {
        "gban": "\
**Modules:** __Global Banned__\n\n**Perintah:** `.gban`\
\n**Penjelasan:** Melakukan Banned Secara Global Ke Semua Grup Dimana Anda Sebagai Admin\
\n\n**Perintah:** `.ungban`\
\n**Penjelasan:** Membatalkan Global Banned"
    }
)
