import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '8292424940:AAEr5MTWVTKRyihejsFwj0ZZigMs63GL4yk'
MANAGER_URL = 'https://t.me/ScamONshop'
PRIVACY_POLICY_URL = 'https://telegra.ph/POLITIKA-KONFIDENCIALNOSTI-01-02-28'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

products_data = {
    "item_1": {
        "name": "Скам-Пакет Мамонтов 2026",
        "description": "Список контактов потенциальных жертв с их предпочтениями и финансовыми данными.",
        "price": "2,900 ₽ (150 чел.) / 4,000 ₽ (340 чел.)",
        "image": "https://i.imgur.com/placeholder1.jpg"
    },
    "item_2": {
        "name": "Мастер-Скам: Руководство", 
        "description": "Пошаговая инструкция по созданию фейковых сайтов и обмана через соцсети.",
        "price": "1,500 ₽ (база) / 3,000 ₽ (VIP)",
        "image": "https://i.imgur.com/placeholder2.jpg"
    },
    "item_3": {
        "name": "ВзломПлатежей Pro",
        "description": "Программа для подмены платежных данных и автоматического списания средств.",
        "price": "6,000 ₽",
        "image": "https://i.imgur.com/placeholder3.jpg"
    },
    "item_4": {
        "name": "АнтиБлокиратор v3.0",
        "description": "Сервис маскировки IP-адресов и обхода банов на сайтах.",
        "price": "7,000 ₽",
        "image": "https://i.imgur.com/placeholder4.jpg"
    },
    "item_5": {
        "name": "Схемы Скама",
        "description": "Коллекция самых прибыльных и новых схем обмана.",
        "price": "1,700 ₽ (5 схем) / 3,700 ₽ (15 схем)",
        "image": "https://i.imgur.com/placeholder5.jpg"
    },
    "item_6": {
        "name": "Генератор Фейк-Документов",
        "description": "Программа для создания поддельных паспортов, счетов и сертификатов.",
        "price": "1,500 ₽",
        "image": "https://i.imgur.com/placeholder6.jpg"
    },
    "item_7": {
        "name": "Бот-Скамер (AI версия)",
        "description": "Чат-бот для автоматического общения с жертвами и сбора данных.",
        "price": "9,000 ₽",
        "image": "https://i.imgur.com/placeholder7.jpg"
    },
    "item_8": {
        "name": "Спам-Мастер",
        "description": "Инструмент для рассылки фишинговых писем.",
        "price": "1,100 ₽",
        "image": "https://i.imgur.com/placeholder8.jpg"
    },
    "item_9": {
        "name": "Шаблоны Фейковых Сайтов",
        "description": "HTML-шаблоны под разные виды обмана.",
        "price": "3,400 ₽",
        "image": "https://i.imgur.com/placeholder9.jpg"
    }
}

def get_main_menu():
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Товар", callback_data="catalog"))
    kb.row(types.InlineKeyboardButton(text="Менеджер", url=MANAGER_URL))
    return kb.as_markup()

def get_catalog_keyboard():
    kb = InlineKeyboardBuilder()
    for item_key, item_info in products_data.items():
        kb.row(types.InlineKeyboardButton(text=f"🌟 {item_info['name']}", callback_data=item_key))
    kb.row(types.InlineKeyboardButton(text="Назад", callback_data="main_menu"))
    return kb.as_markup()

def get_purchase_keyboard(item_key):
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Покупка", callback_data=f"buy_{item_key}"))
    kb.row(types.InlineKeyboardButton(text="Назад в каталог", callback_data="catalog"))
    return kb.as_markup()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = (
        "🚀 **Добро пожаловать в ScamONshop**\n\n"
        "Мы предоставляем лучшие инструменты для работы в сети. "
        "Перед использованием ознакомьтесь с [нашей политикой](" + PRIVACY_POLICY_URL + ").\n\n"
        "Нажимая кнопки ниже, вы принимаете условия."
    )
    
    photo = types.FSInputFile("start_image.jpg")
    await message.answer_photo(
        photo=photo,
        caption=welcome_text, 
        parse_mode="Markdown", 
        reply_markup=get_main_menu()
    )

@dp.callback_query(F.data == "main_menu")
async def handle_back_to_main(callback: types.CallbackQuery):
    await callback.message.answer("Главное меню:", reply_markup=get_main_menu())
    try:
        await callback.message.delete()
    except:
        pass
    await callback.answer()

@dp.callback_query(F.data == "catalog")
async def handle_catalog(callback: types.CallbackQuery):
    catalog_photo = types.FSInputFile("assortiment.jpg")
    await callback.message.answer_photo(
        photo=catalog_photo,
        caption="Наш ассортимент:", 
        reply_markup=get_catalog_keyboard(), 
        parse_mode="Markdown"
    )
    try:
        await callback.message.delete()
    except:
        pass
    await callback.answer()

@dp.callback_query(F.data.startswith("item_"))
async def handle_item_view(callback: types.CallbackQuery):
    selected_item = products_data[callback.data]
    item_text = f"🌟 {selected_item['name']}\n\n😎 {selected_item['description']}\n\n💰 {selected_item['price']}"
    
    await callback.message.answer(
        text=item_text, 
        parse_mode="Markdown", 
        reply_markup=get_purchase_keyboard(callback.data)
    )
    try:
        await callback.message.delete()
    except:
        pass
    await callback.answer()

@dp.callback_query(F.data.startswith("buy_"))
async def handle_payment_info(callback: types.CallbackQuery):
    payment_text = (
        "РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ\n\n"
        "Donation Alerts\n"
        "https://dalink.to/scamonshop\n\n"
        "После перевода нажмите «Перевести», чтобы бот зафиксировал транзакцию.\n\n"
        "(Пишите свой ник при переводе, как у вас в «Телеграме»)"
    )
    payment_kb = InlineKeyboardBuilder()
    payment_kb.row(types.InlineKeyboardButton(text="Перевести", callback_data="done_payment"))
    await callback.message.answer(payment_text, parse_mode="Markdown", reply_markup=payment_kb.as_markup())
    await callback.answer()

@dp.callback_query(F.data == "done_payment")
async def handle_payment_confirm(callback: types.CallbackQuery):
    confirm_text = (
        "Платёж в обработке\n\n"
        "Для подтверждения и получения товара напишите менеджеру. "
        "Прикрепите скриншот чека."
    )
    manager_kb = InlineKeyboardBuilder()
    manager_kb.row(types.InlineKeyboardButton(text="Менеджер", url=MANAGER_URL))
    await callback.message.answer(confirm_text, parse_mode="Markdown", reply_markup=manager_kb.as_markup())
    await callback.answer()
    
    asyncio.create_task(start_order_process(callback.from_user.id))

async def start_order_process(user_id):
    await asyncio.sleep(60)
    
    initial_text = (
        "**Ваш товар собирается** ✅\n"
        "⬇️\n"
        "Ваш товар готовится\n"
        "⬇️\n"
        "Отправка товара\n\n"
        "_Схема для наглядного просмотра покупателем о подготовке и выдаче его товара_"
    )
    
    message = await bot.send_message(user_id, initial_text, parse_mode="Markdown")
    await bot.pin_chat_message(user_id, message.message_id)
    
    await asyncio.sleep(15)
    
    second_text = (
        "Ваш товар собирается ✅\n"
        "⬇️\n"
        "**Ваш товар готовится** ✅\n"
        "⬇️\n"
        "Отправка товара\n\n"
        "_Схема для наглядного просмотра покупателем о подготовке и выдаче его товара_"
    )
    
    await bot.edit_message_text(second_text, user_id, message.message_id, parse_mode="Markdown")
    
    await asyncio.sleep(15)
    
    final_text = (
        "Ваш товар собирается ✅\n"
        "⬇️\n"
        "Ваш товар готовится ✅\n"
        "⬇️\n"
        "**Отправка товара** ✅\n\n"
        "_Схема для наглядного просмотра покупателем о подготовке и выдаче его товара_"
    )
    
    await bot.edit_message_text(final_text, user_id, message.message_id, parse_mode="Markdown")

async def run_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_bot())
# === Это чтобы Render не выключил бота ===
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_ping_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("", port), PingHandler)
    server.serve_forever()

Thread(target=start_ping_server).start()
# =========================================
