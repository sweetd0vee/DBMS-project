# -*- coding: utf-8 -*-
import telebot
import config
from telebot import types
from data_handler import SQLiter
from datetime import datetime

bot = telebot.TeleBot(config.API_TOKEN)

markup_menu = types.InlineKeyboardMarkup(row_width=1)
btn_client = types.InlineKeyboardButton('Просмотреть заказы клиента', callback_data='client')
btn_courier = types.InlineKeyboardButton('Узнать расписание курьера', callback_data='courier')
btn_delivery = types.InlineKeyboardButton('Получить информациию по заказу', callback_data='order')
btn_product = types.InlineKeyboardButton('Добавить товар в каталог', callback_data='add product')
btn_editorder = types.InlineKeyboardButton('Редактировать заказ', callback_data='edit order')
markup_menu.add(btn_client, btn_courier, btn_delivery, btn_product, btn_editorder)

markup_menu1 = types.InlineKeyboardMarkup()
btn_address = types.InlineKeyboardButton('Адрес доставки', callback_data='address')
btn_payment = types.InlineKeyboardButton('Способ оплаты', callback_data='payment')
markup_menu1.add(btn_address, btn_payment)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Добро пожаловать! Выберете действие, которое хотите совершить: /start', reply_markup=markup_menu)


@bot.callback_query_handler(func=lambda call:True)
def call_back_order(call):
    if call.data == 'order':
        bot.send_message(call.message.chat.id, 'Введите ID заказа')
        order_summary_info()
    elif call.data == 'client':
        bot.send_message(call.message.chat.id, 'Введите ID клиента')
        get_client_info()
    elif call.data == 'courier':
        bot.send_message(call.message.chat.id, 'Чтобы узнать расписание курьера, введите его ID,'
                                               'начало и конец временного промежутка в формате  yyyy-mm-dd h:mm\n'
                                               'Пример ввода: 1, 2020-12-15 7:00, 2020-12-30 17:00')
        get_courier_timetable_info()
    elif call.data == 'add product':
        bot.send_message(call.message.chat.id, 'Введите следующие характеристики товара:'
                                               'Артикул, бренд, сезон, размер, пол, тип, цвет, материал, цена, '
                                               'страна производства, ID поставщика')
        add_product2()
    elif call.data == 'edit order':
        bot.send_message(call.message.chat.id, 'Выберите, что хотите изменить:', reply_markup=markup_menu1)
    elif call.data == 'address':
        bot.send_message(call.message.chat.id, 'Введите ID заказа и новый адрес')
        change_address1()
    elif call.data == 'payment':
        bot.send_message(call.message.chat.id, 'Введите ID заказа и желаемый способ оплаты')
        change_payment1()


def change_payment1():
    @bot.message_handler(content_types=['text'])
    def change_payment2(message):
        s = message.text.split(', ')
        db = SQLiter(config.database_name)
        result = db.change_payment(s[0], s[1])
        if result == 0:
            bot.send_message(message.chat.id, 'Ошибка! Заказа с таким ID не найдено.')
        else:
            bot.send_message(message.chat.id, 'Метод оплаты успешно изменен.')
            parc = db.get_parcels(s[0])
            for c in parc:
                bot.send_message(message.chat.id, 'ID заказа: ' + str(c[0]) + '\nID посылки: ' + str(c[1]) +
                                 '\nСпособ оплаты: ' + str(c[2]) + '\n')


def change_address1():
    @bot.message_handler(content_types=['text'])
    def change_address2(message):
        s = message.text.split(', ')
        db = SQLiter(config.database_name)
        result = db.change_address(s[0], s[1])
        if result == 0:
            bot.send_message(message.chat.id, 'Ошибка! Заказа с таким ID не найдено.')
        elif result == 1:
            bot.send_message(message.chat.id, 'Ошибка! Неверный адрес.')
        else:
            bot.send_message(message.chat.id, 'Адрес успешно изменен.')
            addr = db.get_address(s[0])
            for c in addr:
                bot.send_message(message.chat.id, 'ID заказа: ' + str(c[0]) + '\nID посылки: ' + str(c[1]) +
                                 '\nАдрес доставки: ' + str(c[2]) + '\n')


def add_product2():
    @bot.message_handler(content_types=['text'])
    def add_product1(message):
        description = message.text.split(', ')
        db = SQLiter(config.database_name)
        result = db.add_product(description)
        if result == 1:
            bot.send_message(message.chat.id, 'Товар успешно добавлен в каталог.')
            catal = db.get_product_info(description[0])
            bot.send_message(message.chat.id, 'Продукт с артикулом ' + str(catal[0][0]) +
                             ' присутствует в каталоге и имеет тип ' + str(catal[0][1]))
        else:
            bot.send_message(message.chat.id, 'Ошибка! Уже есть товар с таким артикулом.')


def get_courier_timetable_info():
    @bot.message_handler(content_types=['text'])
    def courier_timetable(message):
        s = message.text.split(', ')
        start = datetime.strptime(s[1], '%Y-%m-%d %H:%M')
        end = datetime.strptime(s[2], '%Y-%m-%d %H:%M')
        db = SQLiter(config.database_name)
        timetable = db.get_courier_timetable(s[0], start, end)
        if len(timetable) == 0:
            bot.send_message(message.chat.id, 'Нет поставок в заданный промежуток времени.')
        else:
            for c in timetable:
                info = 'Время доставки с ' + str(c[0]) + ' по ' + str(c[1]) + '\nID посылки: '\
                 + str(c[2]) + '\nСпособ доставки: ' + str(c[3]) + '\nАдрес: ' + str(c[4]) + '\nИмя клиента: '+ str(c[5])
                bot.send_message(message.chat.id, info)


def get_client_info():
    @bot.message_handler(content_types=['text'])
    def client_info(message):
        db = SQLiter(config.database_name)
        order = db.get_client_purchases(message.text)
        if len(order) == 0:
            bot.send_message(message.chat.id, 'Нет клиента с таким ID.')
        else:
            for c in order:
                info = 'ID заказа: ' + str(c[0]) + '\nID товара: ' + str(c[1]) + '\nТип товара: '\
                             + str(c[2]) + '\nЦена: ' + str(c[3]) + 'руб. \nКоличество: ' + str(c[4])
                bot.send_message(message.chat.id, info)


def order_summary_info():
    @bot.message_handler(content_types=['text'])
    def order_summary(message):
        db = SQLiter(config.database_name)
        order = db.get_order_summary(message.text)
        print(order)
        if len(order) == 0:
            bot.send_message(message.chat.id, 'Нет заказа с таким ID.')
        else:
            for c in order:
                info = 'ID заказа: ' + str(c[0]) + '\nСумма заказа: ' + str(c[1]) + ' руб. \nСкидка: '\
                             + str(c[2]) + '% \nИмя клиента: ' + str(c[4]) + '\nНомер теленфона: ' + str(c[5])
                bot.send_message(message.chat.id, info)

bot.polling()
