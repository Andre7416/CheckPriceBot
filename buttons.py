from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


help_btn = KeyboardButton("/help")
sub_btn = KeyboardButton("/subscribe")
unsub_btn = KeyboardButton("/unsubscribe")
add_btn = KeyboardButton("/add")
clear_btn = KeyboardButton("/clear")
pop_btn = KeyboardButton("/remove")
list_btn = KeyboardButton("/list")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).row(sub_btn, help_btn, unsub_btn)
main_menu.row(add_btn, pop_btn)
main_menu.row(list_btn, clear_btn)
