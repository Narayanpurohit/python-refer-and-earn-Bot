import time
import os
import json
import telebot

##TOKEN DETAILS
TOKEN = "INR"

BOT_TOKEN = "6909761308:AAEcUrZ1CsvKaL-9wJZcgN1nR072_rGDhQ4"
PAYMENT_CHANNEL = "@jn_bots"  # add payment channel here including the '@' sign
OWNER_ID = 6789146594  # write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = ["@jn_bots"]  # add channels to be checked here in the format - ["Channel 1", "Channel 2"]
# you can add as many channels here and also add the '@' sign before channel username
Daily_bonus = 10  # Put daily bonus amount here!
Mini_Withdraw = 0.5  # remove 0 and add the minimum withdraw u want to set
Per_Refer = 0.0001  # add per refer bonus here
NEW_USER_BONUS = 5  # add new user bonus here!

bot = telebot.TeleBot(BOT_TOKEN)

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '🎁 Bonus', '💸 Withdraw')
    keyboard.row('⚙️ Set Wallet', '📊 Statistics')
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == '/start':
            user = str(user)
            data = json.load(open('users.json', 'r'))
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
                # Add new user bonus
                data['balance'][user] += NEW_USER_BONUS
                bot.send_message(user, f"🎉 Congratulations! You received {NEW_USER_BONUS} {TOKEN} as a new user bonus.")
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = "0"
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - "
            for i in CHANNELS:
                msg_start += f"\n➡️ {i}\n"
            msg_start += "*"
            bot.send_message(user, msg_start,
                             parse_mode="Markdown", reply_markup=markup)
        else:
            data = json.load(open('users.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
                # Add new user bonus
                data['balance'][user] += NEW_USER_BONUS
                bot.send_message(user, f"🎉 Congratulations! You received {NEW_USER_BONUS} {TOKEN} as a new user bonus.")
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            markups = telebot.types.InlineKeyboardMarkup()
            markups.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
            bot.send_message(user, msg_start,
                             parse_mode="Markdown", reply_markup=markups)
    except:
        bot.send_message(message.chat.id, "This command having error pls wait for fixing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: " + message.text)
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch == True:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(
                    callback_query_id=call.id, text='✅ You joined Now you can earn money')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user not in data['refer']:
                    data['refer'][user] = True
                    if user not in data['referby']:
                        data['referby'][user] = user
                        json.dump(data, open('users.json', 'w'))
                    if int(data['referby'][user]) != user_id:
                        ref_id = data['referby'][user]
                        ref = str(ref_id)
                        if ref not in data['balance']:
                            data['balance'][ref] = 0
                        if ref not in data['referred']:
                            data['referred'][ref] = 0
                        json.dump(data, open('users.json', 'w'))
                        data['balance'][ref] += Per_Refer
                        data['referred'][ref] += 1
                        bot.send_message(
                            ref_id, f"*🏧 New Referral on Level 1, You Got : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)

                else:
                    return menu(call.message.chat.id)

            else:
                bot.answer_callback_query(
                    callback_query_id=call.id, text='❌ You not Joined')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(
                    text='🤼‍♂️ Joined', callback_data='check'))
                msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
                bot.send_message(call.message.chat.id, msg_start,
                                 parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(call.message.chat.id, "This command having error pls wait for fixing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: " + call.data)
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 Account':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 User : {}\n\n⚙️ Wallet : *`{}`*\n\n💸 Balance : *`{}`* {}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"

            json.dump(data, open('users.json', 'w'))

            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name,
                                wallet, balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        if message.text == '🙌🏻 Referrals':
            data = json.load(open('users.json', 'r'))
            ref_msg = "*⏯️ Total Invites : {} Users\n\n👥 Refferrals System\n\n1 Level:\n🥇 Level°1 - {} {}\n\n🔗 Referral Link ⬇️\n{}*"

            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['referred']:
                data['referred'][user] = 0
            json.dump(data, open('users.json', 'w'))

            ref_count = data['referred'][user]
            ref_link = 'https://telegram.me/{}?start={}'.format(
                bot_name, message.chat.id)
            msg = ref_msg.format(ref_count, Per_Refer, TOKEN, ref_link)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        if message.text == "⚙️ Set Wallet":
            user_id = message.chat.id
            user = str(user_id)

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🚫 Cancel')
            send = bot.send_message(message.chat.id, "_⚠️Send your UPI Wallet Address._",
                                    parse_mode="Markdown", reply_markup=keyboard)
            # Next message will call the name_handler function
            bot.register_next_step_handler(send, set_wallet)
        if message.text == '💸 Withdraw':
            user_id = message.chat.id
            user = str(user_id)

            data = json.load(open('users.json', 'r'))
            wallet = data['wallet'][user]
            balance = data['balance'][user]

            if wallet == "none":
                bot.send_message(user_id, "_❌ Set your UPI ID first to proceed with withdrawals._",
                                 parse_mode="Markdown")
                return

            if balance < Mini_Withdraw:
                bot.send_message(user_id, "_❌ Insufficient balance to withdraw._",
                                 parse_mode="Markdown")
                return

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🚫 Cancel')
            send = bot.send_message(message.chat.id, "_⚠️Enter the amount you want to withdraw:_",
                                    parse_mode="Markdown", reply_markup=keyboard)
            bot.register_next_step_handler(send, check_withdraw)
        if message.text == '📊 Statistics':
            user_id = message.chat.id
            user = str(user_id)

            data = json.load(open('users.json', 'r'))
            total_users = data['total']
            total_balance = sum(data['balance'].values())
            total_withdrawn = sum(data['withd'].values())

            stats_msg = "*📊 Bot Statistics*\n\n👥 Total Users: {}\n\n💰 Total Balance: {} {}\n\n💸 Total Withdrawn: {} {}*"
            msg = stats_msg.format(
                total_users, total_balance, TOKEN, total_withdrawn, TOKEN)
            bot.send_message(user_id, msg, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "This command having error pls wait for fixing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: " + message.text)
        return

def set_wallet(message):
    try:
        user_id = message.chat.id
        user = str(user_id)

        if message.text == '🚫 Cancel':
            return menu(user_id)

        data = json.load(open('users.json', 'r'))
        data['wallet'][user] = message.text
        json.dump(data, open('users.json', 'w'))

        bot.send_message(user_id, "_✅ Your UPI ID has been set successfully._",
                         parse_mode="Markdown")
        return menu(user_id)
    except:
        bot.send_message(message.chat.id, "This command having error pls wait for fixing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: " + message.text)
        return

def check_withdraw(message):
    try:
        user_id = message.chat.id
        user = str(user_id)

        if message.text == '🚫 Cancel':
            return menu(user_id)

        amount = float(message.text)
        data = json.load(open('users.json', 'r'))
        balance = data['balance'][user]

        if amount > balance:
            bot.send_message(user_id, "_❌ Withdraw amount exceeds your balance._",
                             parse_mode="Markdown")
            return

        if amount < Mini_Withdraw:
            bot.send_message(user_id, f"_❌ Minimum withdrawal amount is {Mini_Withdraw} {TOKEN}._",
                             parse_mode="Markdown")
            return

        data['balance'][user] -= amount
        data['withd'][user] += amount
        json.dump(data, open('users.json', 'w'))

        bot.send_message(user_id, f"_✅ Withdrawal request for {amount} {TOKEN} submitted successfully._",
                         parse_mode="Markdown")
        return menu(user_id)
    except:
        bot.send_message(message.chat.id, "This command having error pls wait for fixing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: " + message.text)
        return

bot.polling()
