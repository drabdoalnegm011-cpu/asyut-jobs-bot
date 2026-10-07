import os, json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
BOT_TOKEN=os.getenv("BOT_TOKEN")
FILE="jobs.json"
def load():
    try:
        with open(FILE,"r",encoding="utf-8") as f: return json.load(f)
    except: return []
def save(j):
    with open(FILE,"w",encoding="utf-8") as f: json.dump(j,f,ensure_ascii=False,indent=2)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb=[["👷 وظائف","➕ انشر وظيفة"]]
    await update.message.reply_text("بوت وظائف اسيوط شغال ✅\nدوس ➕ انشر وظيفة وهتنزل فوراً بدون موافقة",reply_markup=ReplyKeyboardMarkup(kb,resize_keyboard=True))
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=update.message.text
    if t=="👷 وظائف":
        jobs=load()
        if not jobs:
            await update.message.reply_text("لسه مفيش وظائف")
            return
        await update.message.reply_text("\n\n---\n\n".join(jobs[-10:]))
        return
    if t=="➕ انشر وظيفة":
        await update.message.reply_text("ابعت تفاصيل الوظيفة دلوقتي وهتتنشر فوراً ✅")
        return
    jobs=load(); jobs.append(t); save(jobs)
    await update.message.reply_text(f"✅ اتنشرت فوراً:\n\n{t}")
app=Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle))
app.run_polling()
