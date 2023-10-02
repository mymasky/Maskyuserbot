emoji_categories = [
        "😭",
        "🤬",
        "👀",
        "😎",
        "🖕",
        "👍",
    ]



async def tes(client: Client, message: Message):
        await client.send_reaction(message.chat.id, message.id, random.choice(emoji_categories))
