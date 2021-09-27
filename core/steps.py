# (c) @AbirHasan2005

import os
import json
import inflect as __inflect
from pyrogram import Client
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from core.fix import FixEnvData

inflect = __inflect.engine()
ikeyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Cancel Process", callback_data="cancelProcess")]
            ])


async def StartSteps(bot: Client, editable: Message):
    heroku_app = {
        "name": "",
        "description": "",
        "keywords": list(),
        "repository": "",
        "website": "",
        "success_url": "",
        "env": dict(),
        "buildpacks": list(),
        "formation": dict()
    }
    await editable.edit("**Step 1:**\n"
                        "Send me your Heroku App Name.",
                        reply_markup=ikeyboard)
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["name"] = input_m.text
    await input_m.delete(True)
    await editable.edit("**Step 2:**\n"
                        "Now send me your Heroku App Description.",
                        reply_markup=ikeyboard)
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["description"] = input_m.text
    await input_m.delete(True)
    await editable.edit("**Step 3:**\n"
                        "Now send me your Heroku App Keywords.\n"
                        "Separate using comma(`,`)",
                        reply_markup=ikeyboard)
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["keywords"] = input_m.text.replace(" ", "").split(",")
    await input_m.delete(True)
    await editable.edit("**Step 4:**\n"
                        "Now send me your GitHub Repository Link.",
                        reply_markup=ikeyboard)
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["repository"] = input_m.text
    await input_m.delete(True)
    await editable.edit("**Step 5:**\n"
                        "Now send me your Website Link.",
                        reply_markup=ikeyboard)
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["website"] = input_m.text
    await input_m.delete(True)
    await editable.edit("**Step 6:**\n"
                        "Now send me your Success URL.",
                        reply_markup=ikeyboard)
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["success_url"] = input_m.text
    await input_m.delete(True)
    await editable.edit("**Step 7:**\n"
                        "Now time for ENV configs!\n\n"
                        "When done press /done",
                        reply_markup=ikeyboard)
    env_inputs_running = True
    env_count = 1
    while env_inputs_running:
        await editable.reply_text(f"Send me {inflect.ordinal(env_count)} ENV name & value.\n\n"
                                  "**Note:** __ENV name without <space> and\n"
                                  "use (__`:`__) to define description, value, required, generator respectively.__")
        input_m: Message = await bot.listen(editable.chat.id, timeout=600)
        if input_m.text.startswith("/done"):
            env_inputs_running = False
            continue
        input_str = input_m.text.split(":", 5)
        env_count += 1
        if len(input_str) < 5:
            while len(input_str) < 5:
                input_str.append("")
        input_str = await FixEnvData(input_str)
        heroku_app["env"] = {
            f"{input_str[0].upper()}": {
                "description": f"{input_str[1]}",
                "required": f"{input_str[3]}"
            }
        }
        if input_str[2] != "":
            heroku_app["env"][f"{input_str[0].upper()}"]["value"] = f"{input_str[2]}"
        if input_str[4] != "":
            heroku_app["env"][f"{input_str[0].upper()}"]["generator"] = f"{input_str[4]}"
        await input_m.delete(True)
    await editable.edit("**Step 8:**\n"
                        "Now send Heroku App [Buildpacks](https://telegra.ph/Heroku-Default-Buildpacks-09-27) list.\n"
                        "Separate with (`|`)",
                        reply_markup=ikeyboard)
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    input_buildpacks = input_m.text.split("|")
    for i in range(len(input_buildpacks)):
        heroku_app["buildpacks"].append({"url": f"{input_buildpacks[i]}"})
    await input_m.delete(True)
    await editable.edit("**Step 9:**\n"
                        "What type of process?\n"
                        "Send [`web`] or [`worker`]",
                        reply_markup=ikeyboard)
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    process_type = input_m.text.lower().strip()
    if process_type not in ["web", "worker"]:
        process_type = "worker"
    heroku_app["formation"][f"{process_type}"] = {}
    await input_m.delete(True)
    await editable.edit("**Step 10:**\n"
                        "What will be Dyno Type?\n"
                        "Send [`free`] or [`hobby`] or [`standard-1x`] or "
                        "[`standard-2x`] or [`performance-m`] or [`performance-l`]\n\n"
                        "[Official Documentation](https://devcenter.heroku.com/articles/dyno-types)",
                        reply_markup=ikeyboard)
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    dyno_type = input_m.text.lower()
    if dyno_type not in ["free", "hobby", "standard-1x", "standard-2x", "performance-m", "performance-l"]:
        dyno_type = "free"
    heroku_app["formation"][f"{process_type}"] = {
        "quantity": 1,
        "size": f"{dyno_type}"
    }
    await editable.edit("Making `app.json` ...")
    app_json = f"./downloads/{str(editable.chat.id)}/{str(editable.message_id)}/"
    if not os.path.exists(app_json):
        os.makedirs(app_json)
    js = json.dumps(heroku_app, sort_keys=True, indent=4, separators=(',', ': '))
    with open(f"{app_json}/app.json", "w+") as f:
        f.write(js)
    return f"{app_json}/app.json"
