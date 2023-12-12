import os

from TelethonKiara.plugins import *


@kiara_cmd(pattern="mytweet(?:\s|$)([\s\S]*)")
async def tweet(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, "Tweeting ...")
    if text:
        tweeter = await event.client.inline_query(
            "TwitterStatusBot", f"{(deEmojify(text))}"
        )
        owo = await tweeter[0].click(Config.LOGGER_ID)
        stcr = await event.client.send_message(event.chat_id, owo)
        await kiara.delete()
        await owo.delete()
        await unsave_stcr(event, stcr)
        await unsave_stcr(event, owo)


@kiara_cmd(pattern="trump(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, "Trump is making a tweet ...")
    tweet = await trumptweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await kiara.delete()
    os.remove(tweet)


@kiara_cmd(pattern="modi(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, "Modi is making a tweet ...")
    tweet = await moditweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await kiara.delete()
    os.remove(tweet)


@kiara_cmd(pattern="mia(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, "Mia is making a tweet ...")
    tweet = await miatweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await kiara.delete()
    os.remove(tweet)


@kiara_cmd(pattern="dani(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, "Dani is making a tweet ...")
    tweet = await dani(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await kiara.delete()
    os.remove(tweet)


@kiara_cmd(pattern="pappu(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, "Pappu is making a tweet ...")
    tweet = await papputweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await kiara.delete()
    os.remove(tweet)


@kiara_cmd(pattern="sunny(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, "Sunny is making a tweet ...")
    tweet = await sunnytweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await kiara.delete()
    os.remove(tweet)


@kiara_cmd(pattern="johhny(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, "Johhny is making a tweet ...")
    tweet = await sinstweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await kiara.delete()
    os.remove(tweet)


@kiara_cmd(pattern="gandhi(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, "Gandhi is making a tweet ...")
    tweet = await taklatweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await kiara.delete()
    os.remove(tweet)


@kiara_cmd(pattern="tweet(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    username = None
    if len(lists) == 2:
        if reply and reply.message:
            text = reply.message
            username = lists[1].strip()
        else:
            query = lists[1].split("-", 1)
            username = query[0].strip()
            text = query[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    kiara = await eor(event, f"{username} is making a tweet ...")
    tweet = await mytweet(username, deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await kiara.delete()
    os.remove(tweet)


@kiara_cmd(pattern="cmm(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to change my mind.")
    kiara = await eor(event, "Change my mind ...")
    mind = await changemymind(deEmojify(text))
    await event.client.send_file(event.chat_id, mind, reply_to=reply)
    await kiara.delete()
    os.remove(mind)


@kiara_cmd(pattern="kanna(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to kanna.")
    kiara = await eor(event, "Kanna is writting ...")
    kanna = await kannagen(deEmojify(text))
    await event.client.send_file(event.chat_id, kanna, reply_to=reply)
    await kiara.delete()
    os.remove(kanna)


CmdHelp("tweets").add_command(
    "kanna", "<text>/<reply to text>", "Kanna writes for you"
).add_command(
    "cmm", "<text>/<reply>", "Get a banner of Change My Mind"
).add_command(
    "johhny", "<text>/<reply>", "Tweet with Johhny Sins"
).add_command(
    "sunny", "<text>/<reply>", "Tweet with Sunny Leone"
).add_command(
    "gandhi", "<text>/<reply>", "Tweet with Mahatma Gandhi"
).add_command(
    "pappu", "<text>/<reply>", "Tweet with pappu A.K.A Rahul Gandhi"
).add_command(
    "mia", "<text>/<reply>", "Tweet with Mia Khalifa 😍"
).add_command(
    "trump", "<text>/<reply>", "Tweet with Mr. DooLand Trump"
).add_command(
    "modi", "<text>/<reply>", "Tweet with Sir Narendra Modi"
).add_command(
    "tweet", "<username> - <text/reply to text>", "Tweets in given username."
).add_command(
    "mytweet", "<text or reply to text>", "Tweets with your telegram account name."
).add_command(
    "dani", "<text>/<reply>", "Tweet with Dani Daniels 😍🥰"
).add_info(
    "Lets Tweet."
).add_warning(
    "✅ Harmless Module."
).add()
