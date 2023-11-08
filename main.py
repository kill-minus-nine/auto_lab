import os
from dotenv import load_dotenv
from tg_bot import TgBot
from lab_cycle import lab_cycle

load_dotenv()


def try_read_int_from_env(key, default_value):
    val = os.getenv(key)
    if val is None or not val:
        return default_value
    return int(val)


lab_cycle(
    retry_count_after_refresh=try_read_int_from_env('RETRY_COUNT_AFTER_REFRESH', 7),
    fight_duration_sec=try_read_int_from_env('FIGHT_DURATION_SEC', 10 * 60),
    fight_check_period_sec=try_read_int_from_env('FIGHT_CHECK_PERIOD_SEC', 5),
    tg_bot=TgBot(os.getenv('TG_BOT_API_TOKEN'), os.getenv('FORCE_TG_USER_ID'))
)
