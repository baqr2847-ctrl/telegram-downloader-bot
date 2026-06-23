import os
import re
import base64
import yt_dlp
import requests


PLATFORMS = {
    'tiktok': [r'tiktok\.com', r'vm\.tiktok\.com'],
    'instagram': [r'instagram\.com', r'instagr\.am'],
    'youtube': [r'youtube\.com', r'youtu\.be'],
    'twitter': [r'twitter\.com', r'x\.com'],
    'facebook': [r'facebook\.com', r'fb\.watch', r'fb\.com'],
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def detect_platform(url):
    for platform, patterns in PLATFORMS.items():
        for p in patterns:
            if re.search(p, url, re.I):
                return platform
    return None


def ytdl_download(url, platform):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        'socket_timeout': 20,
        'retries': 2,
        'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},
    }

    if platform == 'instagram':
        ydl_opts['extractor_args'] = {'instagram': {'api': ['mobile']}}
        ydl_opts['add_headers'] = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    cookies_map = {
        'tiktok': ('TIKTOK_COOKIES_B64', 'tiktok_cookies.txt'),
        'instagram': ('INSTAGRAM_COOKIES_B64', 'instagram_cookies.txt'),
    }
    cookie_src = cookies_map.get(platform)
    if cookie_src:
        env_name, file_name = cookie_src
        env_val = os.getenv(env_name)
        if env_val:
            try:
                decoded = base64.b64decode(env_val).decode()
                cpath = os.path.join(os.path.dirname(__file__), f'_{file_name}')
                with open(cpath, 'w', encoding='utf-8') as f:
                    f.write(decoded)
                ydl_opts['cookiefile'] = cpath
            except:
                pass
        else:
            cookies_path = os.path.join(os.path.dirname(__file__), file_name)
            if os.path.exists(cookies_path):
                ydl_opts['cookiefile'] = cookies_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', f'Video from {platform}')[:100]
        formats = info.get('formats', [])

        if not formats:
            if info.get('url'):
                return {'success': True, 'url': info['url'], 'title': title, 'platform': platform}
            return None

        best_url = None
        for fmt in formats:
            ext = fmt.get('ext', '')
            vcodec = fmt.get('vcodec', 'none')
            filesize = fmt.get('filesize') or fmt.get('filesize_approx') or 0
            if ext in ('mp4', 'webm') and vcodec != 'none':
                if filesize and 0 < filesize < 48 * 1024 * 1024:
                    best_url = fmt.get('url')
                    if best_url:
                        break
                elif not filesize:
                    best_url = fmt.get('url')
                    if best_url:
                        break

        if not best_url:
            for fmt in reversed(formats):
                url_candidate = fmt.get('url')
                if url_candidate:
                    best_url = url_candidate
                    break

        if not best_url:
            return None

        return {'success': True, 'url': best_url, 'title': title, 'platform': platform}


def instagram_fallback(url):
    # Try yt-dlp with mobile API
    try:
        opts = {
            'quiet': True, 'no_warnings': True, 'extract_flat': False, 'skip_download': True, 'socket_timeout': 30,
            'extractor_args': {'instagram': {'api': ['mobile']}},
            'add_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            },
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Instagram Video')[:100]
            for fmt in info.get('formats', []):
                if fmt.get('vcodec') != 'none' and fmt.get('ext') in ('mp4', 'webm') and fmt.get('url'):
                    return {'success': True, 'url': fmt['url'], 'title': title, 'platform': 'instagram'}
            if info.get('url'):
                return {'success': True, 'url': info['url'], 'title': title, 'platform': 'instagram'}
    except:
        pass

    # Try Instagram CDN directly via oEmbed
    try:
        code_match = re.search(r'(?:reel|p)/([A-Za-z0-9_-]+)', url)
        if code_match:
            code = code_match.group(1)
            resp = requests.get(
                f'https://i.instagram.com/api/v1/media/{code}/info/',
                headers={
                    'User-Agent': 'Instagram 123.0.0.21.115 Android',
                    'Accept': '*/*',
                },
                timeout=15,
            )
            data = resp.json()
            items = data.get('items', [])
            if items:
                vid_versions = items[0].get('video_versions', [])
                if vid_versions:
                    return {'success': True, 'url': vid_versions[0]['url'], 'title': 'Instagram Video', 'platform': 'instagram'}
    except:
        pass

    # Try third-party downloader APIs
    for api_url in [
        f'https://instasave.io/api/?url={url}',
        f'https://api.socialdownloader.com/api/v1/instagram?url={url}',
        f'https://indown.io/api/info?url={url}',
    ]:
        try:
            resp = requests.get(api_url, headers=HEADERS, timeout=15)
            data = resp.json()
            vid = data.get('url') or data.get('video') or data.get('download_url')
            if vid:
                return {'success': True, 'url': vid, 'title': 'Instagram Video', 'platform': 'instagram'}
            if data.get('medias'):
                for m in data['medias']:
                    if m.get('type') == 'video' and m.get('url'):
                        return {'success': True, 'url': m['url'], 'title': 'Instagram Content', 'platform': 'instagram'}
        except:
            pass

    return None


def tiktok_fallback(url):
    try:
        resp = requests.get(f'https://www.tikwm.com/api/?url={url}', headers=HEADERS, timeout=15)
        data = resp.json()
        if data.get('code') == 0 and data.get('data'):
            video_url = data['data'].get('play') or data['data'].get('wmplay') or data['data'].get('hdplay')
            if video_url:
                return {'success': True, 'url': video_url, 'title': data['data'].get('title', 'TikTok Video')[:100], 'platform': 'tiktok'}
    except:
        pass

    try:
        resp = requests.post('https://api.tikmate.app/api/lookup', data={'url': url}, headers=HEADERS, timeout=10)
        data = resp.json()
        if data and data.get('urls'):
            for item in data['urls']:
                if item.get('type') == 'video' and item.get('url'):
                    return {'success': True, 'url': item['url'], 'title': 'TikTok Video', 'platform': 'tiktok'}
    except:
        pass

    return None


def twitter_fallback(url):
    tweet_id_match = re.search(r'status/(\d+)', url)
    tweet_id = tweet_id_match.group(1) if tweet_id_match else ''

    try:
        resp = requests.get(f'https://api.vxtwitter.com/i/api/status/{tweet_id}', headers=HEADERS, timeout=10)
        data = resp.json()
        if data:
            for media in data.get('media_extended', []):
                if media.get('type') == 'video' and media.get('url'):
                    return {'success': True, 'url': media['url'], 'title': 'Twitter Video', 'platform': 'twitter'}
            if data.get('video_url'):
                return {'success': True, 'url': data['video_url'], 'title': 'Twitter Video', 'platform': 'twitter'}
    except:
        pass

    try:
        resp = requests.get(f'https://twitsave.com/info?url={url}', headers={**HEADERS, 'Accept': 'application/json'}, timeout=10)
        data = resp.json()
        if data.get('video'):
            return {'success': True, 'url': data['video'], 'title': 'Twitter Video', 'platform': 'twitter'}
    except:
        pass

    return None


def facebook_fallback(url):
    try:
        resp = requests.post('https://fbdownloader.net/api/ajaxSearch',
            data={'url': url, 'lang': 'en'},
            headers={**HEADERS, 'X-Requested-With': 'XMLHttpRequest'},
            timeout=20
        )
        data = resp.json()
        if data.get('video'):
            return {'success': True, 'url': data['video'], 'title': 'Facebook Video', 'platform': 'facebook'}
    except:
        pass

    try:
        resp = requests.get(f'https://api.socialdownloader.com/api/v1/facebook?url={url}', headers=HEADERS, timeout=15)
        data = resp.json()
        if data.get('video'):
            return {'success': True, 'url': data['video'], 'title': 'Facebook Video', 'platform': 'facebook'}
    except:
        pass

    return None


FALLBACKS = {
    'instagram': instagram_fallback,
    'tiktok': tiktok_fallback,
    'twitter': twitter_fallback,
    'facebook': facebook_fallback,
}


def download_media(url):
    platform = detect_platform(url)
    if not platform:
        return {
            'success': False,
            'error': 'رابط غير مدعوم. الروابط المدعومة:\n• TikTok\n• Instagram\n• YouTube\n• Twitter / X\n• Facebook'
        }

    try:
        return ytdl_download(url, platform)
    except yt_dlp.utils.DownloadError as e:
        err_msg = str(e)

        if 'cookies' in err_msg.lower() or 'login required' in err_msg.lower() or 'rate-limit' in err_msg.lower():
            fallback = FALLBACKS.get(platform)
            if fallback:
                result = fallback(url)
                if result:
                    return result
            return {
                'success': False,
                'error': f'تعذر تحميل المحتوى من {platform}. المنصة تمنع التحميل المباشر.'
            }

        if 'Private video' in err_msg:
            return {'success': False, 'error': 'هذا الفيديو خاص ولا يمكن تحميله.'}
        if 'not available to everyone' in err_msg.lower():
            return {'success': False, 'error': 'هذا المحتوى غير متاح في منطقتك (مقيد جغرافياً).'}
        if 'Video unavailable' in err_msg or 'This video is not available' in err_msg:
            return {'success': False, 'error': 'هذا الفيديو غير متاح.'}
        if 'HTTP Error 404' in err_msg:
            return {'success': False, 'error': 'الرابط غير صحيح (404).'}
        if 'Sign in to confirm' in err_msg:
            return {'success': False, 'error': 'هذا المحتوى يتطلب تسجيل الدخول.'}
        if 'copyright' in err_msg.lower():
            return {'success': False, 'error': 'هذا المحتوى محمي بحقوق النشر.'}

        fallback = FALLBACKS.get(platform)
        if fallback:
            result = fallback(url)
            if result:
                return result

        return {'success': False, 'error': f'تعذر تحميل المحتوى من {platform}. تأكد من صحة الرابط.'}

    except Exception as e:
        err = str(e)
        if 'timed out' in err.lower():
            return {'success': False, 'error': 'انتهت مهلة الاتصال. حاول مرة أخرى.'}
        if 'no format' in err.lower():
            return {'success': False, 'error': 'لا توجد صيغة مناسبة للتحميل.'}

        fallback = FALLBACKS.get(platform)
        if fallback:
            result = fallback(url)
            if result:
                return result

        return {'success': False, 'error': f'حدث خطأ غير متوقع: {err[:100]}'}
