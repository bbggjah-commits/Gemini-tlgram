import os
import logging
import asyncio
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
logger = logging.getLogger(__name__)

class GeminiTelegramBot:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN غير موجود")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY غير موجود")
        
        # تكوين Gemini API
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # إنشاء تطبيق التلجرام
        self.application = Application.builder().token(self.telegram_token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """إعداد معالجات الأوامر والرسائل"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("about", self.about_command))
        self.application.add_handler(CommandHandler("api_info", self.api_info_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /start"""
        welcome_text = """
🤖 **مرحباً! أنا بوت Gemini AI**

يمكنك التحدث معي مباشرة وسأرد باستخدام الذكاء الاصطناعي المتقدم من Google.

**الأوامر المتاحة:**
/start - بدء المحادثة
/help - عرض التعليمات
/about - معلومات عن البوت
/api_info - كيفية الحصول على API

🚀 **ما عليك سوى إرسال رسالة وسأرد عليك!**
        """
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /help"""
        help_text = """
📖 **دليل استخدام البوت:**

**الأوامر:**
/start - بدء التشغيل
/help - عرض هذه التعليمات  
/about - معلومات عن البوت
/api_info - طريقة الحصول على API

**كيفية الاستخدام:**
1. أرسل أي سؤال أو رسالة
2. انتظر قليلاً mientras يفكر البوت
3. سيصلك رد ذكي من Gemini AI

💡 **نصائح:**
- يمكنك طرح أسئلة بالعربية أو الإنجليزية
- البوت يدعم مواضيع متنوعة
- الرد قد يأخذ بضع ثوانٍ
        """
        await update.message.reply_text(help_text)
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /about"""
        about_text = """
🤖 **معلومات عن البوت**

**الاسم:** Gemini Telegram Bot
**المطور:** [اسمك]
**الإصدار:** 2.0
**التقنية:** Python + GitHub Actions
**النموذج:** Google Gemini Pro

**المميزات:**
✅ تشغيل مستمر عبر GitHub Actions
✅ دعم multilingual
✅ معالجة ذكية للمحادثات
✅ تحديثات تلقائية

🔗 **الكود المصدري:** [رابط GitHub]
        """
        await update.message.reply_text(about_text)
    
    async def api_info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /api_info"""
        api_info = """
🔑 **كيفية الحصول على Gemini API Key:**

1. **اذهب إلى:** [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **سجل الدخول** بحساب Google
3. **انقر على** "Create API Key"
4. **انسخ المفتاح** واحفظه في مكان آمن

**لإعداد البوت:**
1. انسخ المفتاح
2. اذهب إلى إعدادات الريبو على GitHub
3. أضف المفتاح في Secrets كـ `GEMINI_API_KEY`
4. أضف توكن البوت كـ `TELEGRAM_BOT_TOKEN`

⚠️ **مهم:** لا تشارك مفاتيح API الخاصة بك مع أحد!
        """
        await update.message.reply_text(api_info)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة الرسائل النصية من المستخدمين"""
        user_message = update.message.text
        user_name = update.message.from_user.first_name
        
        try:
            # إرسال رسالة انتظار
            wait_message = await update.message.reply_text("🔄 جاري التفكير...")
            
            # توليد الرد باستخدام Gemini
            response = self.model.generate_content(user_message)
            
            # حذف رسالة الانتظار
            await wait_message.delete()
            
            # إرسال الرد مع تقسيم الرسائل الطويلة
            if response.text:
                reply_text = f"🤖 {response.text}"
                
                # تقسيم الرسالة إذا كانت طويلة
                if len(reply_text) > 4096:
                    for i in range(0, len(reply_text), 4096):
                        await update.message.reply_text(reply_text[i:i+4096])
                else:
                    await update.message.reply_text(reply_text)
            else:
                await update.message.reply_text("❌ لم أستطع توليد رد. يرجى المحاولة مرة أخرى.")
                
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")
            await update.message.reply_text("❌ حدث خطأ أثناء معالجة رسالتك. يرجى المحاولة لاحقاً.")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الأخطاء"""
        logger.error(f"Exception while handling an update: {context.error}")
    
    def run(self):
        """تشغيل البوت"""
        logger.info("Starting bot...")
        self.application.run_polling()

if __name__ == '__main__':
    bot = GeminiTelegramBot()
    bot.run()
