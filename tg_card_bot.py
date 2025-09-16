# tg_card_bot.py  — সবাই ব্যবহার করতে পারবে
import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# আপনার বট টোকেন এখানে
TOKEN = "8409937294:AAHt7dw5QoVTARXDJgZSTkJKlPFKupgsWKQ"

# আপনার চ্যানেল লিঙ্ক এখানে
CHANNEL_LINK = "https://t.me/Saydur2147"

ALLOWED_USERS = []  # খালি থাকলে সবাই ব্যবহার করতে পারবে

# --- helpers ---
def luhn_checksum(card_number: str) -> int:
    digits = [int(d) for d in card_number]
    for i in range(len(digits) - 2, -1, -2):
        d = digits[i] * 2
        digits[i] = d if d < 10 else d - 9
    return sum(digits) % 10

def complete_with_luhn(bin_prefix: str, length: int = 16) -> str:
    number = "".join(ch for ch in bin_prefix if ch.isdigit())
    while len(number) < length - 1:
        number += str(random.randint(0, 9))
    if len(number) > length - 1:
        number = number[: length - 1]
    for d in range(10):
        if luhn_checksum(number + str(d)) == 0:
            return number + str(d)
    return number + "0"

def random_expiry(years_ahead=5):
    now = datetime.now()
    future = now + timedelta(days=random.randint(30, 365 * years_ahead))
    return future.strftime("%m"), future.strftime("%Y")

def random_cvv(length=3):
    return "".join(str(random.randint(0, 9)) for _ in range(length))

# --- telegram handlers ---
def start(update: Update, context: CallbackContext):
    msg = (
        "🔗 আমাদের অফিসিয়াল চ্যানেলে যোগ দিন — নিয়মিত আপডেট, রিলিজ ও গুরুত্বপূর্ণ তথ্য পেতে এখনই যুক্ত হোন।\n"
        f"👉 {CHANNEL_LINK}\n\n"
        "ব্যবহার: /gen <pattern> — উদাহরণ: /gen 12345678xxxxxx"
    )
    update.message.reply_text(msg, parse_mode="Markdown")

def gen(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        return update.message.reply_text("Usage: /gen <pattern>\nউদাহরণ: /gen 12345678xxxxxx")
    pattern = args[0]

    results = []
    for _ in range(10):  # প্রতিবার 10টি জেনারেট করবে
        temp = []
        for ch in pattern:
            if ch.lower() == "x":
                temp.append(str(random.randint(0, 9)))
            elif ch.isdigit():
                temp.append(ch)
            # অন্য অক্ষর উপেক্ষা করা হবে

        part = "".join(temp)
        card = complete_with_luhn(part, length=16)
        mm, yyyy = random_expiry()
        cvv = random_cvv()
        results.append(f"{card}|{mm}|{yyyy}|{cvv}")

    update.message.reply_text("\n\n".join(results))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gen", gen))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
