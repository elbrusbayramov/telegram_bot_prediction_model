from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import prediction_model as model
from private_data import TOKEN
import logging

logging.basicConfig(level=logging.INFO)

my_bot = Bot(TOKEN)
my_dispathcer = Dispatcher(my_bot)

guest_passenger_info = {
    'Pclass': 3,
    'Age': 70.0,
    'Parch': 1,
    'Fare': 7.25,
    'Sex_female': 0,
    'Sex_male': 1
}

# buttons  to collect passenger class info from telegram users
p_class1_btn = InlineKeyboardButton(text="Passenger Class 1", callback_data="1")
p_class2_btn = InlineKeyboardButton(text="Passenger Class 2", callback_data="2")
p_class3_btn = InlineKeyboardButton(text="Passenger Class 3", callback_data="3")
p_class_keyboard_inline = InlineKeyboardMarkup().add(p_class1_btn).add(p_class2_btn).add(p_class3_btn)


@my_dispathcer.message_handler(commands=["class"])
async def get_p_class(message: types.Message):
    await message.reply("Your class:", reply_markup=p_class_keyboard_inline)


@my_dispathcer.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Hi,"
                         "\nThis bot will predict if you would survive on the Titanic."
                         "\nLet's imagine you on the board of the Titanic."
                         "\nPlease provide some data:"
                         "\n\n/age"
                         "\n\n/gender"
                         "\n\n/class"
                         "\n\n/predict"
                         )






male_btn = InlineKeyboardButton(text="male",callback_data="male")
female_btn = InlineKeyboardButton(text="female",callback_data="female")
sex_keyboard_inline = InlineKeyboardMarkup().add(male_btn).add(female_btn)

@my_dispathcer.message_handler(commands=["gender"])
async def get_sex(message: types.Message):
    await message.reply("Your gender:",reply_markup=sex_keyboard_inline)


@my_dispathcer.message_handler(commands=["age"])
async def get_age(message: types.Message):
    await message.reply("Your age:")

@my_dispathcer.message_handler(commands=["predict"])
async def send_result(message: types.Message):
    my_result = model.predict_me(guest_passenger_info)
    logging.info(f"Predicting for user with data:{guest_passenger_info}")
    await message.answer(f'You {my_result} !!!')

@my_dispathcer.callback_query_handler(text=["male","female","1","2","3"])
async def get_values(call: types.CallbackQuery):


    if call.data == "male":
        guest_passenger_info["Sex_male"] = 1
        guest_passenger_info["Sex_female"] = 0
        await call.message.answer("Gender male saved")

    elif call.data == "female":
        guest_passenger_info["Sex_male"] = 0
        guest_passenger_info["Sex_female"] = 1
        await call.message.answer("Gender female saved")

    elif call.data == "1":
        guest_passenger_info["Pclass"] = 1
        await call.message.answer("Passenger class 1 saved")

    elif call.data == "2":
        guest_passenger_info["Pclass"] = 2
        await call.message.answer("Passenger class 2 saved")

    elif call.data == "3":
        guest_passenger_info["Pclass"] = 3
        await call.message.answer("Passenger class 3 saved")

    await call.answer()


@my_dispathcer.message_handler()
async  def get_age_value(message:types.Message):
    guest_passenger_info["Age"] = float(message.text)
    await message.answer(f'Age {message.text} saved')

def main():
    executor.start_polling(my_dispathcer)


if __name__ == '__main__':
    main()
