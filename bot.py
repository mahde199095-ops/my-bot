import requests
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
import time

BOT_TOKEN = '8904777258:AAFVwHcKF48xYrrqyzCWQ2rkGJLydIp4L9s'
VT_API_KEY = '7221a26e6da13540ac054d6cfd3e4e12c6f723dd2a04b9d7f101c4a22ff84994'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("⏳ جاري الفحص في VirusTotal، يرجى الانتظار...")

    headers = {'x-apikey': VT_API_KEY}
    payload = {'url': url}
    
    try:
        # 1. إرسال الرابط للفحص
        response = requests.post('https://www.virustotal.com/api/v3/urls', headers=headers, data=payload)
        
        if response.status_code == 200:
            analysis_id = response.json()['data']['id']
            # 2. انتظار بسيط حتى ينتهي الموقع من الفحص
            time.sleep(2) 
            # 3. جلب نتيجة التقرير
            report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
            report = requests.get(report_url, headers=headers).json()
            stats = report['data']['attributes']['stats']
            
            # 4. الرد بالنتيجة في تليجرام
            result_msg = f"📊 نتائج الفحص:\nضار: {stats['malicious']}\nمشكوك فيه: {stats['suspicious']}\nسليم: {stats['harmless']}"
            await update.message.reply_text(result_msg)
        else:
            await update.message.reply_text("❌ فشل الاتصال بخدمة الفحص.")
            
    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ: {str(e)}")

if name == 'main':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("البوت يعمل الآن ومستعد لاستقبال الروابط...")
    app.run_polling()