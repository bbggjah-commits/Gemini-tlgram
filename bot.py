import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تحميل المتغيرات البيئية
load_dotenv()

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# الحصول على التوكنات من المتغيرات البيئية
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# تكوين Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# أوامر البوت
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'مرحباً! أنا بوت مدعوم بـ Gemini AI. 🚀\n\n'
        'يمكنك التحدث معي مباشرة أو استخدام:\n'
        '/help - لعرض التعليمات\n'
        '/about - لمعلومات عن البوت'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 **أوامر البوت:**

/start - بدء المحادثة
/help - عرض هذه التعليمات
/about - معلومات عن البوت
/api_info - كيفية الحصول على Gemini API

💬 **ببساطة أرسل رسالة وسأرد باستخدام Gemini AI!**
    """
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
🤖 **بوت Gemini للتلجرام**

- المطور: [اسمك]
- الإصدار: 1.0
- المدعوم بـ: Google Gemini AI
- الهدف: تقديم مساعدة ذكية باستخدام الذكاء الاصطناعي
    """
    await update.message.reply_text(about_text)

async def api_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api_info = """
🔑 **كيفية الحصول على Gemini API:**

1. اذهب إلى: https://makersuite.google.com/app/apikey
2. سجل الدخول بحساب Google
3. انقر على "Create API Key"
4. انسخ المفتاح واحفظه
5. أضفه إلى ملف .env كـ:
   GEMINI_API_KEY=your_api_key_here

⚠️ **تحذير:** لا تشارك مفتاح API مع أحد!
    """
    await update.message.reply_text(api_info)

# معالجة الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        # إرسال رسالة "يكتب..." أثناء الانتظار
        typing_message = await update.message.reply_text("🔄 يفكر...")
        
        # الحصول على الرد من Gemini
        response = model.generate_content(user_message)
        
        # حذف رسالة "يكتب..."
        await typing_message.delete()
        
        # إرسال الرد (تقسيم الرسالة الطويلة)
        if response.text:
            if len(response.text) > 4096:
                # تقسيم الرسالة الطويلة
                for i in range(0, len(response.text), 4096):
                    await update.message.reply_text(response.text[i:i+4096])
            else:
                await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("⚠️ لم أستطع توليد رد. حاول مرة أخرى.")
            
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء معالجة طلبك.")

# معالجة الأخطاء
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")

# الدالة الرئيسية
def main():
    # إنشاء التطبيق
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("api_info", api_info_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # بدء البوت
    print("🤖 البوت يعمل...")
    application.run_polling()

if __name__ == '__main__':
    main()
