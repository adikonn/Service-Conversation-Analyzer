from io import BytesIO
from db_work import add_chunk, add_to_faiss

from aiogram import Bot, Dispatcher
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from pydub import AudioSegment
from dairiz import get_diar
from check import check_msg
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TG_token")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        "Привет!\nЯ бот для поиска нарушений РЖД\nОтправь мне запись переговора файликом, или как голосовое сообщение"
    )


@dp.message(F.content_type == ContentType.AUDIO)
async def text_to_speech(message: Message):
    msg = await message.reply("обработка...")
    file = message.audio
    audio = BytesIO()
    await bot.download(file.file_id, audio)
    audio.seek(0)
    text = ""
    buttons = []
    for i, chunk in enumerate(get_diar(audio), 1):
        chunk_id = add_chunk(chunk)
        state, reasons = check_msg(chunk)
        if state == False:
            text += "❌" + chunk
            reason_f = "\n".join(reasons[0].split("\n")[:-2])
            text += f"\n({reason_f})"
        else:
            text += "✔️" + chunk
        text += "\n\n"
        buttons.append(types.InlineKeyboardButton(text=f'{i}',
                                                  callback_data=f'{chunk_id}_{i}'))
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=split_list_to_chunks(buttons))
        await bot.edit_message_text(text, message.chat.id, msg.message_id, parse_mode='html', reply_markup=keyboard)


@dp.callback_query()
async def to_faiss(call: types.CallbackQuery):
    chunk_id, key_id = call.data.split('_')
    add_to_faiss(chunk_id)
    await call.message.reply(f'Чанк №{key_id} добавлен в базу Faiss')


@dp.message(F.content_type == ContentType.VOICE)
async def voice_message_handler(message: Message):
    msg = await message.reply("обработка...")
    voice = message.voice.file_id
    audio = BytesIO()
    await bot.download(voice, audio)
    audio.seek(0)
    text = ""
    for chunk in get_diar(audio):
        text += chunk
        state, reasons = check_msg(chunk)
        if state == False:
            text += "```" + "; ".join(reasons) + "```"
        await bot.edit_message_text(
            text, message.chat.id, msg.message_id, parse_mode="html"
        )


@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == "__main__":
    dp.run_polling(bot)
