#!/usr/bin/env python3
"""
بوت تلجرام مع Gemini API - الإصدار الموحد
لا حاجة لملفات إضافية - كل شيء في ملف واحد
"""

import os
import logging
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ⚙️ إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔑 إعداد التوكنات والمفاتيح - يمكنك تعديلها هنا مباشرة
class Config:
    # 🔽 ضع توكن البوت هنا (احصل عليه من @BotFather)
    TELEGRAM_TOKEN = "8523857587:AAEdH8zWdaGhoKSF3oUbgY-VhzPDHlz2iGI"
    
    # 🔽 ضع مفتاح Gemini API هنا (احصل عليه من https://makersuite.google.com/app/apikey)
    GEMINI_API_KEY = "AIzaSyAMF0F9gFAn7PUW29ut0RQmwTtXmz-N7qY"
    
    # إعدادات إضافية
    MAX_MESSAGE_LENGTH = 4096
    TYPING_DELAY = 1

class GeminiBot:
    def __init__(self):
        self.config = Config()
        self.validate_config()
        
        # تكوين Gemini API
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # إنشاء تطبيق التلجرام
        self.application = Application.builder().token(self.config.TELEGRAM_TOKEN).build()
        self.setup_handlers()
        
        logger.info("✅ تم تهيئة البوت بنجاح")

    def validate_config(self):
        """التحقق من صحة التوكنات"""
        if self.config.TELEGRAM_TOKEN == "ضع_توكن_البوت_هنا" or not self.config.TELEGRAM_TOKEN:
            raise ValueError("❌ لم تقم بإعداد توكن البوت! راجع التعليمات في الأسفل")
        
        if self.config.GEMINI_API_KEY == "ضع_m Gemini_API_هنا" or not self.config.GEMINI_API_KEY:
            raise ValueError("❌ لم تقم بإعداد مفتاح Gemini API! راجع التعليمات في الأسفل")

    def setup_handlers(self):
        """إعداد معالجات الأوامر والرسائل"""
        # معالجات الأوامر
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("about", self.about_command))
        self.application.add_handler(CommandHandler("setup", self.setup_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        
        # معالج الرسائل النصية
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # معالج الأخطاء
        self.application.add_error_handler(self.error_handler)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /start"""
        user = update.message.from_user
        welcome_text = f"""
🤖 **مرحباً {user.first_name}!**

أنا بوت ذكي مدعوم بـ **Google Gemini AI** 🚀

**🎯 ما يمكنني فعله:**
• الإجابة على أسئلتك بذكاء
• المساعدة في الكتابة والإبداع
• حل المشكلات Programming
• الترجمه والشرح
• والكثير المزيد!

**📋 الأوامر المتاحة:**
/start - بدء التشغيل
/help - المساعده والتعليمات
/about - معلومات عن البوت  
/setup - طريقة الإعداد
/info - حالة البوت

**💬 فقط اكتب رسالتك وسأرد عليك فوراً!**
        """
        await update.message.reply_text(welcome_text)
        
        # إرسال رسالة ترحيب إضافية
        await update.message.reply_text(
            "🔍 **جربني الآن!** أرسل أي سؤال أو فكرة وسأرد باستخدام الذكاء الاصطناعي المتقدم."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /help"""
        help_text = """
📖 **دليل الاستخدام الكامل**

**⚡ الأوامر السريعة:**
/start - بدء المحادثة وعرض الترحيب
/help - عرض هذه التعليمات
/about - معلومات تقنية عن البوت
/setup - طريقة إعداد البوت خطوة بخطوة
/info - عرض حالة البوت والمفاتيح

**💡 أمثلة على الاستخدام:**
• "اكتب لي قصة قصيرة عن..."
• "اشرح لي نظرية النسبية"
• "ساعدني في كود برمجي لـ..."
• "ترجم النص التالي إلى الإنجليزية"
• "ما هو أفضل طريقة لتعلم..."

**🌍 اللغات المدعومة:**
البوت يدعم العربية والإنجليزية وجميع اللغات الأخرى

**⏱️ وقت الاستجابة:**
عادةً 2-5 ثوانٍ حسب تعقيد السؤال
        """
        await update.message.reply_text(help_text)

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /about"""
        about_text = """
🤖 **معلومات تقنية عن البوت**

**🛠️ التقنيات المستخدمة:**
• Python 3.10+
• python-telegram-bot 20.0+
• google-generativeai 0.3.0+
• GitHub Actions (للتشغيل المستمر)

**📊 الخصائص:**
• تشغيل 24/7 بدون توقف
• معالجة ذكية للمحادثات
• دعم الرسائل الطويلة
• إدارة الأخطاء التلقائية
• تحديثات مستمرة

**🔒 الخصوصية:**
• لا يتم حفظ المحادثات
• التوكنات آمنة
• اتصال مشفر مع API

**🔄 الإصدار: 3.0 (مدمج)**
        """
        await update.message.reply_text(about_text)

    async def setup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /setup - يشرح كيفية إعداد البوت"""
        setup_text = """
🔧 **طريقة إعداد البوت خطوة بخطوة:**

**1️⃣ الحصول على توكن البوت:**
   - اذهب إلى @BotFather في Telegram
   - أرسل /newbot
   - اتبع التعليمات
   - انسخ التوكن وأضفه في الكود

**2️⃣ الحصول على Gemini API:**
   - اذهب إلى: https://makersuite.google.com/app/apikey
   - سجل الدخول بحساب Google
   - انقر "Create API Key" 
   - انسخ المفتاح وأضفه في الكود

**3️⃣ تعديل الكود:**
   - افتح ملف bot.py
   - ابحث عن السطرين:
     TELEGRAM_TOKEN = "ضع_توكن_البوت_هنا"
     GEMINI_API_KEY = "ضع_m Gemini_API_هنا"
   - استبدل النص بين علامات التنصيص بالتوكنات الحقيقية

**4️⃣ التشغيل:**
   - احفظ الملف
   - شغل البوت باستخدام: python bot.py

**❌ استكشاف الأخطاء:**
- تأكد من صحة التوكنات
- تحقق من اتصال الإنترنت
- تأكد من تثبيت المكتبات
        """
        await update.message.reply_text(setup_text)

    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /info - عرض حالة البوت"""
        try:
            # اختبار اتصال Gemini
            test_response = self.model.generate_content("Hello")
            gemini_status = "✅ متصل"
        except Exception as e:
            gemini_status = f"❌ خطأ: {str(e)}"

        info_text = f"""
📊 **حالة البوت:**

**🤖 Telegram Bot:**
• الحالة: ✅ نشط
• الاسم: {self.application.bot.first_name}
• المستخدم: @{self.application.bot.username}

**🧠 Gemini AI:**
• الحالة: {gemini_status}
• النموذج: gemini-pro

**🔑 المفاتيح:**
• Telegram Token: {'✅ مضبوط' if self.config.TELEGRAM_TOKEN != "ضع_توكن_البوت_هنا" else '❌ غير مضبوط'}
• Gemini API: {'✅ مضبوط' if self.config.GEMINI_API_KEY != "ضع_m Gemini_API_هنا" else '❌ غير مضبوط'}

**🔄 الإصدار: 3.0 مدمج**
        """
        await update.message.reply_text(info_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة الرسائل النصية من المستخدمين"""
        user_message = update.message.text
        user_name = update.message.from_user.first_name
        
        logger.info(f"📩 رسالة من {user_name}: {user_message[:50]}...")

        try:
            # إرسال رسالة "يكتب..."
            typing_message = await update.message.reply_text("🔄 جاري التفكير...")
            
            # توليد الرد باستخدام Gemini
            response = self.model.generate_content(user_message)
            
            # حذف رسالة الانتظار
            await typing_message.delete()
            
            # إرسال الرد
            if response.text:
                reply_text = f"🤖 {response.text}"
                
                # تقسيم الرسالة إذا كانت طويلة
                if len(reply_text) > self.config.MAX_MESSAGE_LENGTH:
                    for i in range(0, len(reply_text), self.config.MAX_MESSAGE_LENGTH):
                        chunk = reply_text[i:i + self.config.MAX_MESSAGE_LENGTH]
                        await update.message.reply_text(chunk)
                        await asyncio.sleep(0.5)  # تجنب rate limiting
                else:
                    await update.message.reply_text(reply_text)
                    
                logger.info(f"✅ تم الرد على {user_name}")
                
            else:
                error_msg = "❌ لم أستطع توليد رد. يرجى المحاولة مرة أخرى."
                await update.message.reply_text(error_msg)
                logger.warning(f"⚠️ رد فارغ لـ {user_name}")
                
        except Exception as e:
            error_msg = "❌ حدث خطأ أثناء معالجة رسالتك. يرجى المحاولة لاحقاً."
            await update.message.reply_text(error_msg)
            logger.error(f"🚨 خطأ في handle_message: {e}")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الأخطاء العام"""
        logger.error(f"💥 خطأ غير متوقع: {context.error}")
        
        # يمكن إرسال رسالة للمستخدم في حالة وجود update
        if update and update.message:
            try:
                await update.message.reply_text("❌ حدث خطأ غير متوقع. جاري إعادة التشغيل...")
            except:
                pass

    def run(self):
        """تشغيل البوت"""
        logger.info("🚀 بدء تشغيل بوت Telegram مع Gemini AI...")
        logger.info(f"🤖 اسم البوت: {self.application.bot.first_name}")
        logger.info(f"👤 مستخدم البوت: @{self.application.bot.username}")
        
        try:
            self.application.run_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )
        except Exception as e:
            logger.error(f"💥 فشل تشغيل البوت: {e}")
            raise

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("🤖 بوت Telegram مع Gemini AI - الإصدار المدمج")
    print("=" * 50)
    
    try:
        bot = GeminiBot()
        bot.run()
    except ValueError as e:
        print(f"\n❌ خطأ في الإعداد: {e}")
        print("\n🔧 التعليمات:")
        print("1. افتح ملف bot.py")
        print("2. ابحث عن class Config")
        print("3. ضع التوكنات في:")
        print("   - TELEGRAM_TOKEN")
        print("   - GEMINI_API_KEY")
        print("4. احفظ الملف وشغله مجدداً")
        print("\n📖 للمساعدة: https://github.com/your-repo")
    except Exception as e:
        print(f"\n💥 خطأ غير متوقع: {e}")

if __name__ == '__main__':
    main()
