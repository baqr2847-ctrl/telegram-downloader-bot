import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'users.json')


def _load():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Storage load error: {e}")
    return {'users': {}, 'stats': {'totalDownloads': 0, 'totalUsers': 0}}


def _save(db):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Storage save error: {e}")


db = _load()


def get_user(user_id):
    uid = str(user_id)
    if uid not in db['users']:
        db['users'][uid] = {
            'id': user_id,
            'first_seen': datetime.now().isoformat(),
            'username': '',
            'banned': False,
            'downloads': 0
        }
        db['stats']['totalUsers'] = len(db['users'])
        _save(db)
    return db['users'][uid]


def is_banned(user_id):
    u = db['users'].get(str(user_id))
    return u['banned'] if u else False


def ban_user(user_id):
    u = get_user(user_id)
    u['banned'] = True
    _save(db)


def unban_user(user_id):
    u = db['users'].get(str(user_id))
    if u:
        u['banned'] = False
        _save(db)


def increment_downloads(user_id):
    u = get_user(user_id)
    u['downloads'] = u.get('downloads', 0) + 1
    db['stats']['totalDownloads'] = db['stats'].get('totalDownloads', 0) + 1
    _save(db)


def update_username(user_id, username):
    u = get_user(user_id)
    if username and u.get('username') != username:
        u['username'] = username
        _save(db)


def get_stats():
    return {
        'totalUsers': db['stats'].get('totalUsers', len(db['users'])),
        'totalDownloads': db['stats'].get('totalDownloads', 0),
        'bannedCount': sum(1 for u in db['users'].values() if u.get('banned'))
    }


def get_all_users():
    return list(db['users'].values())
