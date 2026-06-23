import os
import logging
import asyncio

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from storage import get_user, is_banned, ban_user, unban_user, increment_downloads, update_username, get_stats, get_all_users
from downloader import download_media, detect_platform
from create_welcome import create_welcome_image
import config_manager

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ تأكد من وجود BOT_TOKEN في ملف .env")
    exit(1)

CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', '@z0taw')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'e7_6w')
_welcome_image = None

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)


def get_channel():
    return config_manager.get_channel() or CHANNEL_USERNAME


def get_admin():
    return config_manager.get_admin() or ADMIN_USERNAME


def is_admin(user):
    admin = get_admin()
    return user.username and user.username.lower() == admin.lower()


def get_channel_link():
    ch = get_channel()
    return f"https://t.me/{ch.replace('@', '')}"


async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=get_channel(), user_id=update.effective_user.id)
        if member.status in ('member', 'administrator', 'creator'):
            return True
    except:
        pass
    return False


async def require_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.effective_user):
        return True
    if await check_subscription(update, context):
        return True

    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=get_channel_link())],
        [InlineKeyboardButton("✅ تم الاشتراك", callback_data='check_sub')]
    ]
    await update.message.reply_text(
        f"🚫 <b>عذراً، يجب عليك الاشتراك في القناة لاستخدام البوت!</b>\n\n📢 اشترك الآن: {get_channel()}\n\n↩️ بعد الاشتراك، اضغط على زر ✓",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return False


def get_welcome_image_path():
    custom = config_manager.get_welcome_image()
    if custom:
        return custom
    return None


async def welcome_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global _welcome_image
    text = (
        "🎉 <b>مرحباً بك في بوت التحميل الشامل!</b> 🎉\n\n"
        "📥 <b>أرسل لي رابط فيديو من أي منصة وسأقوم بتحميله لك!</b>\n\n"
        "🌐 <b>المنصات المدعومة:</b>\n"
        "• 🎵 TikTok\n"
        "• 📸 Instagram\n"
        "• 🎬 YouTube\n"
        "• 🐦 Twitter / X\n"
        "• 📘 Facebook\n\n"
        "💡 <b>فقط أرسل الرابط وسأقوم بالباقي!</b>"
    )

    img = get_welcome_image_path()
    if img and os.path.exists(img):
        try:
            with open(img, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption=text, parse_mode='HTML')
            return
        except:
            pass

    if _welcome_image is None or not os.path.exists(_welcome_image):
        _welcome_image = create_welcome_image()
    try:
        with open(_welcome_image, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=text, parse_mode='HTML')
    except:
        await update.message.reply_text(text, parse_mode='HTML')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    update_username(user.id, user.username)
    if not await require_subscription(update, context):
        return
    await welcome_user(update, context)


async def check_sub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if await check_subscription(update, context):
        await query.delete_message()
        await welcome_user(update, context)
    else:
        await query.answer("❌ لم يتم الاشتراك بعد! اشترك بالقناة ثم اضغط على الزر.", show_alert=True)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    update_username(user.id, user.username)
    if not await require_subscription(update, context):
        return
    text = (
        f"📖 <b>مساعدة البوت</b>\n\n"
        f"🎯 <b>كيفية الاستخدام:</b>\n"
        f"• أرسل أي رابط فيديو من المنصات المدعومة\n"
        f"• انتظر قليلاً وسيتم تحميل الفيديو لك\n\n"
        f"🌐 <b>المنصات المدعومة:</b>\n"
        f"• TikTok - روابط tiktok.com / vm.tiktok.com\n"
        f"• Instagram - روابط instagram.com\n"
        f"• YouTube - روابط youtube.com / youtu.be\n"
        f"• Twitter / X - روابط twitter.com / x.com\n"
        f"• Facebook - روابط facebook.com / fb.watch\n\n"
        f"👑 <b>الأوامر:</b>\n"
        f"/start - بدء البوت\n"
        f"/help - عرض المساعدة\n\n"
        f"🔒 يجب الاشتراك في {get_channel()} لاستخدام البوت."
    )
    await update.message.reply_text(text, parse_mode='HTML')


def admin_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 الإحصائيات", callback_data='adm_stats'),
         InlineKeyboardButton("👥 المستخدمين", callback_data='adm_users'),
         InlineKeyboardButton("⚙️ الإعدادات", callback_data='adm_settings')],
        [InlineKeyboardButton("📢 إذاعة", callback_data='adm_broadcast'),
         InlineKeyboardButton("🖼 تغيير الصورة", callback_data='adm_setphoto'),
         InlineKeyboardButton("🔄 استعادة الصورة", callback_data='adm_resetphoto')],
        [InlineKeyboardButton("📝 تغيير القناة", callback_data='adm_setchannel'),
         InlineKeyboardButton("👤 تغيير المطور", callback_data='adm_setadmin')],
        [InlineKeyboardButton("🚫 حظر", callback_data='adm_ban'),
         InlineKeyboardButton("✅ إلغاء حظر", callback_data='adm_unban')],
        [InlineKeyboardButton("🔄 تحديث", callback_data='adm_refresh')],
    ])


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    stats = get_stats()
    adm = get_admin()
    ch = get_channel()
    text = (
        "👑 <b>لوحة التحكم</b>\n\n"
        f"📊 <b>الإحصائيات:</b>\n"
        f"👥 إجمالي المستخدمين: {stats['totalUsers']}\n"
        f"📥 إجمالي التحميلات: {stats['totalDownloads']}\n"
        f"🚫 المحظورين: {stats['bannedCount']}\n\n"
        f"⚙️ <b>الإعدادات الحالية:</b>\n"
        f"📢 القناة: {ch}\n"
        f"👑 المطور: @{adm}\n\n"
        f"🛠 اختر من الأزرار أدناه:"
    )
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=admin_keyboard())


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return
    stats = get_stats()
    text = (
        f"📊 <b>إحصائيات البوت</b>\n\n"
        f"👥 إجمالي المستخدمين: {stats['totalUsers']}\n"
        f"📥 إجمالي التحميلات: {stats['totalDownloads']}\n"
        f"🚫 المحظورين: {stats['bannedCount']}"
    )
    await update.message.reply_text(text, parse_mode='HTML')


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    adm = get_admin()
    ch = get_channel()
    img = get_welcome_image_path()
    img_status = "✅ موجودة" if img and os.path.exists(img) else "❌ غير موجودة (سيتم استخدام الصورة الافتراضية)"

    text = (
        "⚙️ <b>الإعدادات الحالية</b>\n\n"
        f"📢 <b>القناة:</b> {ch}\n"
        f"👑 <b>المطور:</b> @{adm}\n"
        f"🖼 <b>صورة الترحيب:</b> {img_status}\n\n"
        "🛠 <b>لتغيير:</b>\n"
        "/setchannel [قناة] - تغيير القناة\n"
        "/setadmin [يوزر] - تغيير المطور\n"
        "/setphoto - تعيين صورة ترحيبية جديدة\n"
        "/resetphoto - استعادة الصورة الافتراضية"
    )
    await update.message.reply_text(text, parse_mode='HTML')


async def set_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("❌ استخدام: /setchannel <معرف القناة>\nمثال: /setchannel @mychannel")
        return

    channel = args[0].strip()
    if not channel.startswith('@'):
        channel = '@' + channel

    config_manager.set_channel(channel)
    await update.message.reply_text(f"✅ تم تغيير القناة إلى {channel} بنجاح.\n🔄 تم حفظ الإعداد.")


async def set_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("❌ استخدام: /setadmin <يوزر>\nمثال: /setadmin username")
        return

    admin = args[0].strip().lstrip('@')
    config_manager.set_admin(admin)
    await update.message.reply_text(f"✅ تم تغيير المطور إلى @{admin} بنجاح.")


async def set_photo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text(
            "❌ <b>الاستخدام الصحيح:</b>\n"
            "1. أرسل صورة للبوت\n"
            "2. رد على الصورة بـ /setphoto\n\n"
            "أو أرسل /setphoto مع صورة في نفس الرسالة.",
            parse_mode='HTML'
        )
        return

    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    ext = 'png'
    dest = os.path.join(os.path.dirname(__file__), 'data', f'welcome_custom.{ext}')

    await file.download_to_drive(dest)
    config_manager.set_welcome_image(dest)

    await update.message.reply_text("✅ <b>تم تغيير صورة الترحيب بنجاح!</b>", parse_mode='HTML')


async def reset_photo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    config_manager.set_welcome_image('')
    custom = os.path.join(os.path.dirname(__file__), 'data', 'welcome_custom.png')
    if os.path.exists(custom):
        os.remove(custom)

    await update.message.reply_text("✅ تم استعادة صورة الترحيب الافتراضية.")


async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    users = get_all_users()
    if not users:
        await update.message.reply_text("لا يوجد مستخدمين بعد.")
        return

    recent = users[-10:]
    recent.reverse()
    lines = ["📋 <b>آخر 10 مستخدمين:</b>\n"]
    for i, u in enumerate(recent, 1):
        name = f"@{u['username']}" if u.get('username') else f"ID: {u['id']}"
        status = "🚫" if u.get('banned') else "✅"
        date = u.get('first_seen', '')[:10] if u.get('first_seen') else '-'
        lines.append(f"{i}. {status} {name} - {u.get('downloads', 0)} تحميلات - {date}")

    lines.append(f"\n👥 الإجمالي: {len(users)} مستخدم")
    await update.message.reply_text('\n'.join(lines), parse_mode='HTML')


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    text = update.message.text
    cmd = '/broadcast'
    msg = text[len(cmd):].strip()

    if not msg:
        await update.message.reply_text(
            "❌ استخدام: /broadcast <الرسالة>\n"
            "مثال: /broadcast مرحباً بالجميع!"
        )
        return

    users = get_all_users()
    sent = 0
    failed = 0

    status = await update.message.reply_text(f"📢 جاري إرسال الإذاعة إلى {len(users)} مستخدم...")

    for u in users:
        if u.get('banned'):
            continue
        try:
            await context.bot.send_message(
                chat_id=u['id'],
                text=f"📢 <b>رسالة من الإدارة:</b>\n\n{msg}",
                parse_mode='HTML'
            )
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)

    await status.edit_text(
        f"✅ <b>تم الإرسال!</b>\n\n"
        f"📨 تم الإرسال: {sent}\n"
        f"❌ فشل: {failed}\n"
        f"👥 الإجمالي: {len(users)}",
        parse_mode='HTML'
    )


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("❌ استخدام: /ban <معرف المستخدم>\nمثال: /ban 123456789")
        return

    try:
        uid = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ يرجى إدخال معرف مستخدم صحيح.")
        return

    ban_user(uid)
    await update.message.reply_text(f"✅ تم حظر المستخدم {uid} بنجاح.")


async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("❌ هذه الخاصية للمشرفين فقط.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("❌ استخدام: /unban <معرف المستخدم>\nمثال: /unban 123456789")
        return

    try:
        uid = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ يرجى إدخال معرف مستخدم صحيح.")
        return

    unban_user(uid)
    await update.message.reply_text(f"✅ تم إلغاء حظر المستخدم {uid} بنجاح.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    update_username(user.id, user.username)

    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if text.startswith('/'):
        return

    if not await require_subscription(update, context):
        return

    if is_banned(user.id):
        await update.message.reply_text("🚫 تم حظرك من استخدام البوت.")
        return

    platform = detect_platform(text)
    if not platform:
        await update.message.reply_text(
            "❌ <b>رابط غير صالح أو غير مدعوم!</b>\n\n"
            "الروابط المدعومة:\n"
            "• TikTok\n"
            "• Instagram\n"
            "• YouTube\n"
            "• Twitter / X\n"
            "• Facebook\n\n"
            "💡 أرسل /help للمساعدة.",
            parse_mode='HTML'
        )
        return

    status_msg = await update.message.reply_text(
        f"⏳ <b>جاري تحميل الفيديو من {platform}...</b>\nيرجى الانتظار قليلاً.",
        parse_mode='HTML'
    )

    try:
        result = download_media(text)

        if result['success']:
            increment_downloads(user.id)
            await status_msg.delete()

            context.user_data['last_original_url'] = text
            context.user_data['last_platform'] = result['platform']

            caption = (
                f"✅ <b>تم التحميل بنجاح!</b>\n"
                f"📌 المنصة: {result['platform']}\n"
                f"📥 شكراً لاستخدامك البوت!"
            )

            audio_button = InlineKeyboardMarkup([[
                InlineKeyboardButton("🎵 تحويل إلى صوت", callback_data='to_audio')
            ]])

            try:
                await update.message.reply_video(
                    video=result['url'],
                    caption=caption,
                    parse_mode='HTML',
                    supports_streaming=True,
                    reply_markup=audio_button
                )
            except Exception as e:
                err = str(e)
                if 'too large' in err.lower() or '413' in err:
                    await update.message.reply_text(
                        f"❌ <b>الفيديو كبير جداً!</b>\n\n"
                        f"الحد الأقصى لرفع الفيديو هو 50 ميغابايت.\n"
                        f"رابط التحميل المباشر:\n{result['url']}",
                        parse_mode='HTML'
                    )
                else:
                    await update.message.reply_text(
                        f"❌ <b>حدث خطأ أثناء إرسال الفيديو.</b>\n\n"
                        f"رابط التحميل المباشر:\n{result['url']}",
                        parse_mode='HTML'
                    )
        else:
            await status_msg.edit_text(
                f"❌ <b>خطأ في التحميل:</b>\n{result['error']}\n\n"
                f"💡 تأكد من صحة الرابط وحاول مرة أخرى.",
                parse_mode='HTML'
            )

    except Exception as e:
        try:
            await status_msg.edit_text(
                f"❌ <b>حدث خطأ غير متوقع!</b>\nيرجى المحاولة مرة أخرى لاحقاً.",
                parse_mode='HTML'
            )
        except:
            pass


async def convert_to_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    await query.answer()

    original_url = context.user_data.get('last_original_url')
    platform = context.user_data.get('last_platform', 'المصدر')

    if not original_url:
        await query.message.reply_text(
            "❌ <b>لا يوجد فيديو سابق للتحويل!</b>\nقم بتحميل فيديو أولاً ثم استخدم هذا الزر.",
            parse_mode='HTML'
        )
        return

    status = await query.message.reply_text(
        f"🎵 <b>جاري تحويل الفيديو إلى صوت...</b>\n⏳ قد يستغرق ذلك بعض الوقت.",
        parse_mode='HTML'
    )

    import yt_dlp
    import uuid

    temp_dir = os.path.join(os.path.dirname(__file__), 'data', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    temp_id = str(uuid.uuid4())
    temp_path = os.path.join(temp_dir, f'audio_{temp_id}.%(ext)s')
    output_path = os.path.join(temp_dir, f'audio_{temp_id}.mp3')

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([original_url])

        if os.path.exists(output_path):
            with open(output_path, 'rb') as audio_file:
                await context.bot.send_audio(
                    chat_id=user.id,
                    audio=audio_file,
                    title=f"🎵 صوت من {platform}",
                    performer=f"@{user.username or 'User'}",
                    caption=f"✅ <b>تم تحويل الفيديو إلى صوت!</b>\n📌 المنصة: {platform}",
                    parse_mode='HTML'
                )
            await status.delete()
        else:
            await status.edit_text(
                "❌ <b>فشل تحويل الفيديو إلى صوت.</b>\nقد يكون الملف كبيراً جداً.",
                parse_mode='HTML'
            )

    except Exception as e:
        err = str(e)
        if 'ffmpeg' in err.lower():
            await status.edit_text(
                "❌ <b>FFmpeg غير مثبت!</b>\nيرجى تثبيت FFmpeg لتفعيل خاصية التحويل إلى صوت.",
                parse_mode='HTML'
            )
        else:
            await status.edit_text(
                f"❌ <b>حدث خطأ أثناء التحويل:</b>\n{err[:150]}",
                parse_mode='HTML'
            )
    finally:
        for f in [output_path, temp_path.replace('%(ext)s', 'webm'), temp_path.replace('%(ext)s', 'm4a')]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass


async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    if not is_admin(user):
        await query.answer("❌ هذه الخاصية للمشرفين فقط.", show_alert=True)
        return

    await query.answer()
    data = query.data

    if data == 'adm_stats':
        stats = get_stats()
        text = (
            f"📊 <b>إحصائيات البوت</b>\n\n"
            f"👥 إجمالي المستخدمين: {stats['totalUsers']}\n"
            f"📥 إجمالي التحميلات: {stats['totalDownloads']}\n"
            f"🚫 المحظورين: {stats['bannedCount']}"
        )
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=admin_keyboard())

    elif data == 'adm_users':
        users = get_all_users()
        if not users:
            await query.edit_message_text("لا يوجد مستخدمين بعد.", reply_markup=admin_keyboard())
            return
        recent = users[-10:]
        recent.reverse()
        lines = ["📋 <b>آخر 10 مستخدمين:</b>\n"]
        for i, u in enumerate(recent, 1):
            name = f"@{u['username']}" if u.get('username') else f"ID: {u['id']}"
            status = "🚫" if u.get('banned') else "✅"
            date = u.get('first_seen', '')[:10] if u.get('first_seen') else '-'
            lines.append(f"{i}. {status} {name} - {u.get('downloads', 0)} تحميلات - {date}")
        lines.append(f"\n👥 الإجمالي: {len(users)} مستخدم")
        await query.edit_message_text('\n'.join(lines), parse_mode='HTML', reply_markup=admin_keyboard())

    elif data == 'adm_settings':
        adm = get_admin()
        ch = get_channel()
        img = get_welcome_image_path()
        img_status = "✅ موجودة" if img and os.path.exists(img) else "❌ غير موجودة"
        text = (
            "⚙️ <b>الإعدادات الحالية</b>\n\n"
            f"📢 <b>القناة:</b> {ch}\n"
            f"👑 <b>المطور:</b> @{adm}\n"
            f"🖼 <b>صورة الترحيب:</b> {img_status}\n\n"
            "🛠 استخدم الأزرار لتغيير الإعدادات."
        )
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=admin_keyboard())

    elif data == 'adm_broadcast':
        await query.edit_message_text(
            "📢 <b>إرسال إذاعة</b>\n\n"
            "استخدم الأمر التالي:\n"
            "<code>/broadcast رسالتك هنا</code>\n\n"
            "مثال:\n"
            "<code>/broadcast مرحباً بالجميع!</code>",
            parse_mode='HTML', reply_markup=admin_keyboard()
        )

    elif data == 'adm_setphoto':
        await query.edit_message_text(
            "🖼 <b>تغيير صورة الترحيب</b>\n\n"
            "الطريقة:\n"
            "1. أرسل الصورة للبوت\n"
            "2. رد على الصورة بـ <code>/setphoto</code>\n\n"
            "أو يمكنك إرسال <code>/setphoto</code> رداً على صورة.",
            parse_mode='HTML', reply_markup=admin_keyboard()
        )

    elif data == 'adm_resetphoto':
        config_manager.set_welcome_image('')
        custom = os.path.join(os.path.dirname(__file__), 'data', 'welcome_custom.png')
        if os.path.exists(custom):
            os.remove(custom)
        await query.edit_message_text(
            "✅ تم استعادة صورة الترحيب الافتراضية.",
            parse_mode='HTML', reply_markup=admin_keyboard()
        )

    elif data == 'adm_setchannel':
        await query.edit_message_text(
            "📝 <b>تغيير القناة</b>\n\n"
            "استخدم الأمر:\n"
            "<code>/setchannel @username</code>\n\n"
            "مثال:\n"
            "<code>/setchannel @mychannel</code>",
            parse_mode='HTML', reply_markup=admin_keyboard()
        )

    elif data == 'adm_setadmin':
        await query.edit_message_text(
            "👤 <b>تغيير المطور</b>\n\n"
            "استخدم الأمر:\n"
            "<code>/setadmin username</code>\n\n"
            "مثال:\n"
            "<code>/setadmin myadmin</code>",
            parse_mode='HTML', reply_markup=admin_keyboard()
        )

    elif data == 'adm_ban':
        await query.edit_message_text(
            "🚫 <b>حظر مستخدم</b>\n\n"
            "استخدم الأمر:\n"
            "<code>/ban user_id</code>\n\n"
            "مثال:\n"
            "<code>/ban 123456789</code>\n\n"
            "💡 لعرض معرف المستخدمين، استخدم زر المستخدمين.",
            parse_mode='HTML', reply_markup=admin_keyboard()
        )

    elif data == 'adm_unban':
        await query.edit_message_text(
            "✅ <b>إلغاء حظر مستخدم</b>\n\n"
            "استخدم الأمر:\n"
            "<code>/unban user_id</code>\n\n"
            "مثال:\n"
            "<code>/unban 123456789</code>",
            parse_mode='HTML', reply_markup=admin_keyboard()
        )

    elif data == 'adm_refresh':
        stats = get_stats()
        adm = get_admin()
        ch = get_channel()
        text = (
            "👑 <b>لوحة التحكم</b>\n\n"
            f"📊 <b>الإحصائيات:</b>\n"
            f"👥 إجمالي المستخدمين: {stats['totalUsers']}\n"
            f"📥 إجمالي التحميلات: {stats['totalDownloads']}\n"
            f"🚫 المحظورين: {stats['bannedCount']}\n\n"
            f"⚙️ <b>الإعدادات الحالية:</b>\n"
            f"📢 القناة: {ch}\n"
            f"👑 المطور: @{adm}\n\n"
            f"🛠 اختر من الأزرار أدناه:"
        )
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=admin_keyboard())


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_sub_callback, pattern='^check_sub$'))
    app.add_handler(CallbackQueryHandler(convert_to_audio, pattern='^to_audio$'))
    app.add_handler(CallbackQueryHandler(admin_callback, pattern='^adm_'))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("setchannel", set_channel_command))
    app.add_handler(CommandHandler("setadmin", set_admin_command))
    app.add_handler(CommandHandler("setphoto", set_photo_command))
    app.add_handler(CommandHandler("resetphoto", reset_photo_command))
    app.add_handler(CommandHandler("users", users_command))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    ch = get_channel()
    adm = get_admin()
    print(f"✅ بوت التحميل يعمل بنجاح!")
    print(f"  🤖 البوت: @{BOT_TOKEN.split(':')[0]}")
    print(f"  📢 القناة: {ch}")
    print(f"  👑 المطور: @{adm}")
    print("  ⏳ انتظر حتى اكتمال التهيئة...")

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
