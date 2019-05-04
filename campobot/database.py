from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection
from telegram import Bot, Chat, Message, Update, User

# Type hinting
profiles_collection: Collection
reports_collection: Collection
logs_collection: Collection
person_collection: Collection

# User Constants
USER_LASTNAME = u'user_lastname'
USER_USERNAME = u'user_username'
USER_LANGUAGE = u'user_language'
USER_LINK = u'user_link'
USER_ID = u'user_id'
USER_FIRSTNAME = u'user_firstname'

# Chat Constants
CHAT_TYPE = u'chat_type'
CHAT_ID = u'chat_id'

# Profile Constants
INITIAL_USAGE = u'initial_usage'

# Multiple Constants
_ID = u'_id'

# Report Constants
YEAR = u'year'
MONTH = u'month'
HOURS = u'hours'
VIDEOS = u'videos'
RETURNS = u'returns'
STUDIES = u'studies'
PUBLICATIONS = u'publications'

# People Constants
NAME = u'name'
AGE = u'age'
ADDRESS = u'address'
RESPONSIBLE_ID = u'responsible_id'
IS_STUDENT = u'is_student'
NOTES = u'notes'


def startup_mongodb():
    # In case of database read/write bugs remove global variables
    global profiles_collection
    global reports_collection
    global logs_collection
    global people_collection

    # uri = open('campobot/token/token_db_test.txt', 'r').read().strip()
    client = MongoClient()
    db = client['campo']

    campo_collections_names = ['profiles', 'reports', 'logs', 'people']
    # [Check] Create DB and its Collections if it doesn't exists
    if not 'campo' in client.list_database_names():
        for campo_collection_name in campo_collections_names:
            db.create_collection(campo_collection_name)

    # [Check] If it each Collection doesn't exists, create
    for campo_collection_name in campo_collections_names:
        if campo_collection_name not in db.list_collection_names():
            db.create_collection(campo_collection_name)

        # Set variable correctly for each Collection
        if campo_collection_name is 'profiles':
            profiles_collection = db.get_collection(campo_collection_name)
        elif campo_collection_name is 'reports':
            reports_collection = db.get_collection(campo_collection_name)
        elif campo_collection_name is 'logs':
            logs_collection = db.get_collection(campo_collection_name)
        elif campo_collection_name is 'people':
            people_collection = db.get_collection(campo_collection_name)


def save_profile_db(bot: Bot, update: Update):
    usr: User = update.effective_user
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    profiles_collection.update_one(
        filter={_ID: usr.id},
        update={"$set": {
            _ID: usr.id,
            USER_ID: usr.id,
            USER_FIRSTNAME: usr.first_name,
            USER_LASTNAME: usr.last_name,
            CHAT_TYPE: chat.type,
            CHAT_ID: chat.id,
            USER_USERNAME: usr.username,
            USER_LANGUAGE: usr.language_code,
            USER_LINK: usr.link,
            INITIAL_USAGE: datetime.now().timestamp()
        }},
        upsert=True)


def get_profile_list_db():
    profile_list = list(
        profiles_collection.find({})
    )

    return profile_list


def save_cron_db(bot, update, cron_time):
    usr: User = update.effective_user

    reports_collection.update_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        },
        update={u'$inc': {
            HOURS: cron_time
        }},
        upsert=True)


def save_hours_db(update, hours_count):
    usr: User = update.effective_user
    if type(hours_count) is not int:
        raise TypeError('Invalid data type. Expected <int> but found', type(hours_count))

    reports_collection.update_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        },
        update={
            u"$set": {
                HOURS: hours_count
            }},
        upsert=True
    )


def get_hours_db(update):
    usr: User = update.effective_user

    cursor: dict = reports_collection.find_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        }
    )

    if cursor is None:
        return 0
    else:
        if cursor.get(HOURS) is None:
            return 0
        else:
            return cursor.get(HOURS)


def save_videos_db(update, videos_count):
    usr: User = update.effective_user
    if type(videos_count) is not int:
        raise TypeError('Invalid data type. Expected <int> but found', type(videos_count))

    reports_collection.update_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        },
        update={u'$set': {
            VIDEOS: videos_count
        }},
        upsert=True
    )


def get_videos_db(update):
    usr: User = update.effective_user

    cursor: dict = reports_collection.find_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        })

    if cursor is None:
        return 0
    else:
        if cursor.get(VIDEOS) is None:
            return 0
        else:
            return cursor.get(VIDEOS)


def save_pubs_db(update, pubs_count):
    usr: User = update.effective_user

    if type(pubs_count) is not int:
        raise TypeError('Invalid data type. Expected <int> but found', type(pubs_count))

    reports_collection.update_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        },
        update={u'$set': {
            PUBLICATIONS: pubs_count
        }},
        upsert=True
    )


def get_pubs_db(update):
    usr: User = update.effective_user

    cursor: dict = reports_collection.find_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        })

    if cursor is None:
        return 0
    else:
        if cursor.get(PUBLICATIONS) is None:
            return 0
        else:
            return cursor.get(PUBLICATIONS)


def save_returns_db(update, return_count):
    usr: User = update.effective_user

    if type(return_count) is not int:
        raise TypeError('Invalid data type. Expected <int> but found', type(return_count))

    reports_collection.update_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        },
        update={u'$set': {
            RETURNS: return_count
        }},
        upsert=True
    )


def get_returns_db(update):
    usr: User = update.effective_user

    cursor: dict = reports_collection.find_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        })

    if cursor is None:
        return 0
    else:
        if cursor.get(RETURNS) is None:
            return 0
        else:
            return cursor.get(RETURNS)


def get_returns_list_db(update):
    usr: User = update.effective_user

    returns_list = list(people_collection.find({
        RESPONSIBLE_ID: usr.id,
        IS_STUDENT: False
    }).sort(NAME))

    return returns_list


def save_studies_db(update, studies_count):
    usr: User = update.effective_user

    if type(studies_count) is not int:
        raise TypeError('Invalid data type. Expected <int> but found', type(studies_count))

    reports_collection.update_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        },
        update={u'$set': {
            STUDIES: studies_count
        }},
        upsert=True
    )


def get_studies_db(update):
    usr: User = update.effective_user

    cursor: dict = reports_collection.find_one(
        filter={
            USER_ID: usr.id,
            YEAR: datetime.now().year,
            MONTH: datetime.now().month
        })

    if cursor is None:
        return 0
    else:
        if cursor.get(STUDIES) is None:
            return 0
        else:
            return cursor.get(STUDIES)


def get_report_db(update=None, chat_id=None, month=None):
    month_query = datetime.now().month
    year_query = datetime.now().year

    if month is not None:
        month_query = month

        # Handle accordingly if current month is January
        if month == 0:
            month_query = 12
            year_query -= 1

    if update is not None:
        usr: User = update.effective_user

        cursor: dict = reports_collection.find_one(
            filter={
                USER_ID: usr.id,
                YEAR: year_query,
                MONTH: month_query
            })
    else:
        cursor: dict = reports_collection.find_one(
            filter={
                USER_ID: chat_id,
                YEAR: year_query,
                MONTH: month_query
            })

    return cursor
