import redis
from config import Config
import random

db = redis.StrictRedis(host=Config.redis_host,port=Config.redis_port, charset="utf-8", decode_responses=True)

def get_current_album():
    current_album_hash = db.get('current_album_hash')
    current_album = db.hgetall(current_album_hash)
    if current_album == {}:
        current_album = False
        return current_album
    else:
        return current_album

def set_current_album():
    total_submissions = db.llen('submission_list')
    if total_submissions == 0:
        return False
    else:
        new_album_index = random.randint(0,(total_submissions - 1))
        new_album_hash = db.lindex('submission_list', new_album_index)
        db.set('current_album_hash', new_album_hash)
        db.lrem('submission_list',0,new_album_hash)
        db.lpush('previous_submissions',new_album_hash)
        return True
    
def submit_album(submit_dict):
    if submit_dict['user'] == "":
        submit_dict['user'] = "Anonymous"
    hash_number = db.incr('current_submission',amount=1)
    db.hmset(hash_number,submit_dict)
    db.lpush('submission_list',hash_number)
    return True

def submission_names(list_name, start, end):
    hashes_to_name = db.lrange(list_name, start, end)
    named_submissions = []
    for i in hashes_to_name:
        album_title = db.hget(i, 'album_title')
        album_artist = db.hget(i, 'album_artist')
        submit_by = db.hget(i, 'user')
        info = album_artist + " - " + album_title + " {" + submit_by + "}"
        named_submissions.append(info)
    return named_submissions

def db_list_length(list_name):
    length = db.llen(list_name)
    return length
