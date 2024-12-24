import asyncio
import random

# import dp
import requests

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile, InputMediaPhoto
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

Token = '7150509625:AAFS6FaUIwbrgjscLwHhFtxybLKNoJ2xzD0'
channel_username = "@zzayabka"



bot = Bot(token=Token)
dp = Dispatcher()

user_data = {}

email = 'ortiqovabduvoris949@gmail.com'
password = '3hI3zXDRAuMYkdZGHhaKCRT3gxsmScHWF4qCxqCF'

def get_eskiz_token(email, password):
    url = "https://notify.eskiz.uz/api/auth/login"
    payload = {
        'email': email,
        'password': password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get('data', {}).get('token')


def send_sms(phone_number, token):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    payload = {
        'mobile_phone': phone_number,
        'message': f"Bu Eskiz dan test",
        'from': '0707',
        'callback_url': 'http://callback.url/3/1'
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code != 200:
        raise Exception("SMS yuborishda hatolik: " + response.text)

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id=message.from_user.id
    user_data[user_id] = {}
    button = [
        [types.KeyboardButton(text="🇷🇺 Русский"),
        types.KeyboardButton(text="🇺🇿 O'zbekcha")],
        [types.KeyboardButton(text="🇬🇧 English")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f"Здравствуйте! Давайте для начала выберем язык обслуживания!\n \n"
                        f"Salom! Keling, avvaliga xizmat ko’rsatish tilini tanlab olaylik!\n \n"
                        f"Hi! Let's first we choose language of serving!", reply_markup=keyboard)



@dp.message(lambda message: message.text == "🇺🇿 O'zbekcha")
async def rclang(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    button = [
        [types.KeyboardButton(text="📞 Mening raqamim", request_contact=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("😊Assalomu alaykum!\n😉Iltimos, telefon raqamingizni jo'nating.", reply_markup=keyboard)


async def phone_number(message: types.Message):
    user_id = message.from_user.id
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
    user_data[user_id]['phone_number'] = phone
    verification_code = random.randint(1000, 9999)
    user_data[user_id]['status'] = 'not verified'
    user_data[user_id]['verification_code'] = verification_code
    await message.answer(f"Tasdiqlash kodi: {verification_code}")
    print(user_data)


async def check_verification(message: types.Message):
    user_id = message.from_user.id
    code = user_data[user_id]['verification_code']
    if str(code) == message.text:
        user_data[user_id]['status'] = 'verified'
        button = [
            [types.KeyboardButton(text="Mening manzilim🗺", request_location=True)]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Iltimos manzilni jo'nating.🗺", reply_markup=keyboard)
    else:
        await message.reply("❌Noto'g'ri terildi. Iltimos yana urunib ko'ring.😉")
    print(user_data)

async def address(message: types.Message):
    user_id = message.from_user.id
    if message.location:
        user_data[user_id][
            "address"] = f"Latitude: {message.location.latitude}. Longtitude: {message.location.longitude}"
    else:
        user_data[user_id]["address"] = message.text
    print(user_data)
    user_data[user_id]['state'] = "main_menu"
    await show_main_menu(message)

    # await bot.send_message(channel_username)
    # del user_data[user_id]

async def show_main_menu(message: types.Message):
    buttons = [
        [KeyboardButton(text="🍽 Menyu")],
        [KeyboardButton(text="📖 Buyurtmalar tarixi"),
         KeyboardButton(text="✍️ Fikr bildirish")],
        [KeyboardButton(text="ℹ️ Ma'lumot"),
         KeyboardButton(text="☎️ Biz bilan aloqa")],
        [KeyboardButton(text="⚙️ Sozlamalar")],
        [KeyboardButton(text="🧑🏻‍💻 Vakansiyalar - GIOTTO")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Bosh menyu", reply_markup=keyboard)


menu = {
    "🧇 Вафли": {"ВАФЛЯ Клубника+шоколад": {'price': 61.500, 'image': 'vafliqulupnay.jpg'}, "ВАФЛЯ Классическая": {'price': 23.000, 'image': 'vafliklassik.jpg'}, "ВАФЛЯ Банан+Nutella": {'price': 52.000, 'image': 'vaflibanan.jpg'}},
    "🥐 Фондю": {"Фондю со свежей клубникой": {'price': 261.000, 'image': 'fonduqulupnay.jpg'}, "Фондю с профитролями": {'price': 205.000, 'image': 'fondus.jpg'}, "Фондю ассорти": {'price': 236.500, 'image': 'fonduassorti.jpg'}},
    "🍨 Мороженое": {"OREO (Пломбир, шоколад)": {'price': 275.000, 'image': 'oreo.jpg'}, "BANANA (Банан молочный) ": {'price': 275.000,  'image': 'banan.jpg'}, "CHEESE CAKE": {'price': 275.000, 'image': 'chizkeyk.jpg'}},
    "🥤 Меню бар": {"ЧАЙ ЭРЛ ГРЕЙ": {'price': 19.000, 'image': 'choy.jpg'}, "КОФЕ ДАБЛ АМЕРИКАНО": {'price': 21.000, 'image': 'kofe.jpg'}, "ДЕТОКС МЯТА-КИВИ": {'price': 40.000, 'image': 'smuzi.jpg'}},
    "🍝 Ресторан": {"Паста Фетучини Альфредо": {'price': 85.000, 'image': 'pasta.jpg'}, "Говяжьи Медальоны с баклажановой Меланзана": {'price': 163.000, 'image': 'gosh.jpg'}, "Чикен-бургер ": {'price': 66.000, 'image': 'burger.jpg'}}
}


@dp.message(lambda message: message.text == "ℹ️ Ma'lumot")
async def info(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'info'}
    buttons = [
        [KeyboardButton(text="🗺Ресторан С1 г.Ташкент ,Ц1 ул.Шахрисабз 33а (ор-р г-ца Тата)")],
        [KeyboardButton(text="⬅️ Ortga")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Sizni qaysi filial qiziqtiryapti?", reply_markup=keyboard)
    print(user_data)

@dp.message(lambda message: message.text == "⚙️ Sozlamalar")
async def nastroyki(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'nastroyki'}
    await message.answer("Siz nimanidir o'zgartirishga haqqiz yo'q. Chunki bu botning hech qanday hatosi yo'q. Hato faqat sizda. Auf💥💥💥")
    if user_data[user_id]['state'] == 'nastroyki':
        await show_main_menu(message)
    print(user_data)

@dp.message(lambda message: message.text == "🗺Ресторан С1 г.Ташкент ,Ц1 ул.Шахрисабз 33а (ор-р г-ца Тата)")
async def restaurant(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'restaurant'}
    await message.answer("Filial joylashuvi: https://yandex.uz/maps/org/91294368591/?ll=69.284277%2C41.330615&z=14")
    if user_data[user_id]['state'] == 'restaurant':
        await show_main_menu(message)
    print(user_data)

@dp.message(lambda message: message.text == "☎️ Biz bilan aloqa")
async def contact_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'contact_uz'}
    await message.answer("Agar sizda savollar bo'lsa bizga yozishingiz mumkin: @Giottoadmins_bot")
    if user_data[user_id]['state'] == 'contact_uz':
        await show_main_menu(message)
    print(user_data)

@dp.message(lambda message: message.text == "🧑🏻‍💻 Vakansiyalar - GIOTTO")
async def vacation_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'vacation_uz'}
    await message.answer("Vakansiyalar – GIOTTO: @giottovacations")
    if user_data[user_id]['state'] == 'vacation_uz':
        await show_main_menu(message)
    print(user_data)

@dp.message(lambda message: message.text == "✍️ Fikr bildirish")
async def feedback_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'feedback_uz'}
    buttons = [
        [KeyboardButton(text="😊 Hammasi yoqdi, 5 ⭐️⭐️⭐️⭐️⭐️")],
        [KeyboardButton(text="☺️ Yaxshi, 4 ⭐️⭐️⭐️⭐️")],
        [KeyboardButton(text="😐 Yoqmadi, 3 ⭐️⭐️⭐️")],
        [KeyboardButton(text="☹️ Yomon, 2 ⭐️⭐️")],
        [KeyboardButton(text="😤 Juda yomon 👎🏻")],
        [KeyboardButton(text="⬅️ Ortga")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("✅ GIOTTOni tanlaganingiz uchun rahmat.\nAgar Siz bizning hizmatlarimiz sifatini yaxshilashga yordam bersangiz, bundan benihoya xursand bo'lamiz.Buning uchun 5 ballik tizim asosida baholang", reply_markup=keyboard)
    print(user_data)

@dp.message(lambda message: message.text == '😊 Hammasi yoqdi, 5 ⭐️⭐️⭐️⭐️⭐️')
async def feedback5_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'feedback5_uz'}
    await message.reply("Fikr-mulohazalaringiz uchun tashakkur!\nShuningdek, siz matnli yoki audio xabar shaklida fikr qoldirishingiz mumkin: @Giottoadmins_bot")
    if user_data[user_id]['state'] == 'feedback5_uz':
        await show_main_menu(message)
    print(user_data)

@dp.message(lambda message: message.text == "☺️ Yaxshi, 4 ⭐️⭐️⭐️⭐️")
async def feedback4_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'feedback4_uz'}
    buttons = [
        [KeyboardButton(text="📦 Mahsulot")],
        [KeyboardButton(text="ℹ️ Xizmat"),
        KeyboardButton(text="🛵 Yetkazib berish")],
        [KeyboardButton(text="⬅️ Ortga")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.reply("Qaysi xizmat turimiz sizga ko'proq YOQMADI?", reply_markup=keyboard)
    print(user_data)

@dp.message(lambda message: message.text == "😐 Yoqmadi, 3 ⭐️⭐️⭐️")
async def feedback3_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'feedback3_uz'}
    button = [
        [KeyboardButton(text="📦 Mahsulot")],
        [KeyboardButton(text="ℹ️ Xizmat"),
        KeyboardButton(text="🛵 Yetkazib berish")],
        [KeyboardButton(text="⬅️ Ortga")]
    ]
    keyboar = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True, one_time_keyboard=True)
    await message.reply("Qaysi xizmat turimiz sizga ko'proq YOQMADI?", reply_markup=keyboar)
    print(user_data)

@dp.message(lambda message: message.text == "☹️ Yomon, 2 ⭐️⭐️")
async def feedback2_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'feedback2_uz'}
    buttons = [
        [KeyboardButton(text="📦 Mahsulot")],
        [KeyboardButton(text="ℹ️ Xizmat"),
        KeyboardButton(text="🛵 Yetkazib berish")],
        [KeyboardButton(text="⬅️ Ortga")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.reply("Qaysi xizmat turimiz sizga ko'proq YOQMADI?", reply_markup=keyboard)
    print(user_data)

@dp.message(lambda message: message.text == "😤 Juda yomon 👎🏻")
async def feedback_end_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'feedback_end_uz'}
    buttons = [
        [KeyboardButton(text="📦 Mahsulot")],
        [KeyboardButton(text="ℹ️ Xizmat"),
        KeyboardButton(text="🛵 Yetkazib berish")],
        [KeyboardButton(text="⬅️ Ortga")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.reply("Qaysi xizmat turimiz sizga ko'proq YOQMADI?", reply_markup=keyboard)
    print(user_data)

@dp.message(lambda message: message.text == '📦 Mahsulot')
async def product_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'product_uz'}
    await message.reply("Fikr-mulohazalaringiz uchun tashakkur!\nShuningdek, siz matnli yoki audio xabar shaklida fikr qoldirishingiz mumkin: @Giottoadmins_bot")
    if user_data[user_id]['state'] == 'product_uz':
        await show_main_menu(message)
    print(user_data)

@dp.message(lambda message: message.text == 'ℹ️ Xizmat')
async def service_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'service_uz'}
    await message.reply("Fikr-mulohazalaringiz uchun tashakkur!\nShuningdek, siz matnli yoki audio xabar shaklida fikr qoldirishingiz mumkin: @Giottoadmins_bot")
    if user_data[user_id]['state'] == 'service_uz':
        await show_main_menu(message)
    print(user_data)

@dp.message(lambda message: message.text == '🛵 Yetkazib berish')
async def courier_uz(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'state': 'courier_uz'}
    await message.reply("Fikr-mulohazalaringiz uchun tashakkur!\nShuningdek, siz matnli yoki audio xabar shaklida fikr qoldirishingiz mumkin: @Giottoadmins_bot")
    if user_data[user_id]['state'] == 'courier_uz':
        await show_main_menu(message)
    print(user_data)

@dp.message(lambda message: message.text == "⬅️ Ortga")
async def go_back(message: types.Message):
    user_id = message.from_user.id
    if user_data[user_id]['state'] == 'feedback_uz':
        await show_main_menu(message)
    elif user_data[user_id]['state'] == 'feedback4_uz':
        await feedback_uz(message)
    elif user_data[user_id]['state'] == 'feedback3_uz':
        await feedback_uz(message)
    elif user_data[user_id]['state'] == 'feedback2_uz':
        await feedback_uz(message)
    elif user_data[user_id]['state'] == 'feedback_end_uz':
        await feedback_uz(message)
    if user_data[user_id]['state'] == 'info':
        await show_main_menu(message)


async def check_main_menu(message: types.Message):
    user_id = message.from_user.id
    if message.text == "🍽 Menyu":
        user_data[user_id]['state'] = "food_menu"
        await show_food_menu(message)
    elif message.text == "📖 Buyurtmalar tarixi":
        await finish_order(message)
    print(user_data)


async def show_food_menu(message: types.Message):
    user_id = message.from_user.id
    buttons = []
    for category in menu:
        buttons.append([KeyboardButton(text=category)])

    buttons.append([KeyboardButton(text="Orqaga⬅")])
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Nimadan boshlimiz?🙃", reply_markup=keyboard)


async def check_food_menu(message: types.Message):
    user_id = message.from_user.id
    if message.text in menu:
        category = message.text
        user_data[user_id]['current_category'] = category
        await show_items(message, category)
    elif message.text == 'Orqaga⬅':
        user_data[user_id]['state'] = 'main_menu'
        await show_main_menu(message)
    elif message.text == 'Savatni tozalash🧹':
        await clean_basket(message)
    print(user_data)


async def clean_basket(message: types.Message):
    user_id = message.from_user.id
    if 'basket' in user_data[user_id]:
        user_data[user_id]['basket'] = {}
        await message.answer("Savat tozalandi.✔")
    else:
        await message.answer("Savat allaqachon bo'sh.😯")
    await show_food_menu(message)


async def show_items(message: types.Message, category: str):
    user_id = message.from_user.id
    buttons = []
    for item in menu[category]:
        buttons.append([KeyboardButton(text=item)])
    buttons.append([KeyboardButton(text="Orqaga⬅")])
    user_data[user_id]['state'] = "item_selection"
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Nimadan boshlimiz?🙃", reply_markup=keyboard)
    print(user_data)


async def check_item_selection(message: types.Message):
    user_id = message.from_user.id
    category = user_data[user_id]['current_category']
    if message.text in menu[category]:
        item = message.text
        price = menu[category][item]['price']
        photo_path = menu[category][item]['image']
        photo = FSInputFile(photo_path)

        buttons = [
            [InlineKeyboardButton(text="Savatga qo'shish➕", callback_data=f"add_{item}")]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer_photo(photo=photo, caption=f"{item}\n\n\nPrice: {price} sum", reply_markup=keyboard)

    elif message.text == 'Orqaga⬅':
        user_data[user_id]['state'] = "food_menu"
        await show_food_menu(message)

    print(user_data)

async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data.startswith("add_"):
        item = data.split("_")[1]
        if 'basket' not in user_data[user_id]:
            user_data[user_id]['basket'] = {}
        if item in user_data[user_id]['basket']:
            user_data[user_id]['basket'][item] += 1
        else:
            user_data[user_id]['basket'][item] = 1

        await callback_query.message.answer(f"{item} savatga qo'shildi!")
        await callback_query.answer()

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await start(message)
    elif 'phone_number' not in user_data[user_id]:
        await phone_number(message)
    elif 'not verified' in user_data[user_id]['status']:
        await check_verification(message)
    elif 'address' not in user_data[user_id]:
        await address(message)
    elif user_data[user_id]['state'] == "main_menu":
        await check_main_menu(message)
    elif user_data[user_id]['state'] == "food_menu":
        await check_food_menu(message)
    elif user_data[user_id]['state'] == "item_selection":
        await check_item_selection(message)
    elif message.text == "Savatni ko'rish":
        await show_cart(message)

@dp.callback_query(lambda c: c.data.startswith(('add_', 'increase_', 'decrease_')))
async def item_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    action, item = callback_query.data.split('_')
    if 'basket' in user_data[user_id]:
        basket = user_data[user_id]['basket']
    else:
        basket = {}
    category = user_data[user_id]['current_category']
    price = menu[category][item]['price']
    if action == 'add' or action == 'increase':
        if item in basket:
            basket[item] += 1
        else:
            basket[item] = 1
    elif action == 'decrease':
        if item in basket and basket[item] > 0:
            basket[item] -= 1
    user_data[user_id]['basket'] = basket
    quantity = basket.get(item, 0)
    total_price = price * quantity
    buttons = [
            [InlineKeyboardButton(text="-", callback_data=f"decrease_{item}"),
            InlineKeyboardButton(text=f"{quantity}", callback_data=f"count_{item}"),
            InlineKeyboardButton(text="+", callback_data=f"increase_{item}")],
           [InlineKeyboardButton(text="Savatga qo'shish➕", callback_data=f"add_{item}")],
            [InlineKeyboardButton(text="Savatni tozalash🧹", callback_data=f"clear_cart_{item}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    basket_summary = await get_basket_summary(user_id)

    photo_path = menu[category][item]['image']
    photo = FSInputFile(photo_path)
    media = InputMediaPhoto(
        media=photo,
        caption=f"{item}\n\n\nPrice: {price} sum\nSoni: {quantity}\nSavat:{basket_summary}"
    )
    await bot.edit_message_media(
        media=media,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard
    )

async def get_basket_summary(user_id):
    basket = user_data[user_id].get('basket', {})
    summary = []
    total = 0
    for item, quantity in basket.items():
        for category, items in menu.items():
            if item in items:
                price = items[item]['price']
                total_price = quantity * price
                summary.append(f"Buyurtma tasdiqlandi!✅\n\n{item}: {quantity} x {price} = {total_price}")
                total += total_price
    summary.append(f"\nJami : {total}")
    return "\n".join(summary)

async def finish_order(message: types.Message):
    user_id = message.from_user.id
    if 'basket' in user_data[user_id]:
        basket = user_data[user_id]['basket']
    else:
        basket = {}
    if not basket:
        await message.answer("Savatingiz bo'sh. Uni tezroq to'ldirish kerak!😧")
    total = await get_basket_summary(user_id)
    await message.answer(total)
    user_data[user_id]['basket'] = {}
    user_data[user_id]['state'] = 'main_menu'
    print(user_data)

async def show_cart(message: types.Message):
    user_id = message.from_user.id
    if 'basket' in user_data[user_id]:
        basket = user_data[user_id]['basket']
    else:
        basket = {}
    if not basket:
        await message.answer("Savatingiz bo'sh. Uni tezroq to'ldirish kerak!😧")
    else:
        cart_summary = await get_basket_summary(user_id)
        buttons = [
            [InlineKeyboardButton(text="Tasdiqlash✔", callback_data="confirm_cart")]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(cart_summary, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "confirm_cart")
async def confirm_cart(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.message.answer("Buyurtma tasdiqlandi!✅")
    user_data[user_id]['basket'] = {}
    user_data[user_id]['state'] = 'ain_menu'
    print(user_data)

@dp.callback_query(lambda c: c.data.startswith("clear_cart_"))
async def clear_cart(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    item = callback_query.data.split("_")[2]
    if 'basket' in user_data[user_id]:
        basket = user_data[user_id]['basket']
        if item in basket:
            del basket[item]
    user_data[user_id]['basket'] = basket
    await callback_query.message.answer(f"{item} savatdan o'chirildi!")
    await callback_query.answer()



async def main():
    print('The bot is running!')
    await dp.start_polling(bot)
asyncio.run(main())