import os
import time
import logging
from bot import GeminiTelegramBot

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """الدالة الرئيسية لتشغيل البوت على GitHub Actions"""
    try:
        logger.info("🚀 بدء تشغيل بوت Telegram مع Gemini AI")
        
        # إنشاء وتشغيل البوت
        bot = GeminiTelegramBot()
        
        logger.info("✅ البوت يعمل بنجاح. جاري الاستماع للرسائل...")
        bot.run()
        
    except Exception as e:
        logger.error(f"❌ خطأ في التشغيل: {e}")
        # إعادة التشغيل بعد 60 ثانية في حالة الفشل
        time.sleep(60)
        main()

if __name__ == '__main__':
    main()
