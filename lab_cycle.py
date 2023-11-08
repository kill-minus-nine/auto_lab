import pyautogui as ag
from time import sleep

NO_RETRY_COUNT = 1


def abort_with_alert(message, bot):
    bot.send_message(message)
    ag.alert(message)
    bot.stop()
    raise RuntimeError(message)


def click(button_names, should_find, retry_count_after_refresh, bot):
    button = None
    retry_cnt = retry_count_after_refresh if should_find else NO_RETRY_COUNT
    for _ in range(retry_cnt):
        for button_name in button_names:
            button = ag.locateCenterOnScreen('samples\\' + button_name + '.png')
            if button is not None:
                break

        if button is None:
            sleep(1)

    if button is not None:
        ag.click(button.x, button.y)
        screen_sizes = ag.size()
        ag.moveTo(screen_sizes.width / 2, screen_sizes.height / 2)
        return True
    elif should_find:
        abort_with_alert(','.join(button_names) + ' button(s) was not found', bot)

    return False


def lab_cycle(retry_count_after_refresh, fight_duration_sec, fight_check_period_sec, tg_bot):
    while ag.locateCenterOnScreen('samples\\hunting.png') is None:
        print('waiting for active dwar window')
        sleep(1)

    first_iter = True
    while True:

        clicked = click(['turn_rychag'], not first_iter, retry_count_after_refresh, tg_bot)

        click(['forward', 'next_floor'], clicked, retry_count_after_refresh, tg_bot)

        click(['come_to_rychag'], True, retry_count_after_refresh, tg_bot)
        # trader:
        # come_to_rychag not found
        # click search_pass
        # next click seq: forward + come_to_rychag

        # statue:
        # come_to_rychag not found
        # click search_pass
        # next click seq: forward + come_to_rychag

        # chest:
        

        sleep(1)

        sure = ag.locateCenterOnScreen('samples\\sure_yes.png')
        if sure is None:
            abort_with_alert('Sure yes button button was not found', tg_bot)
        ag.click(sure.x, sure.y)

        win = None
        for _ in range(int(fight_duration_sec / fight_check_period_sec)):  # 10 min
            win = ag.locateCenterOnScreen('samples\\win.png')
            if win is not None:
                break
            sleep(fight_check_period_sec)

        if win is None:
            abort_with_alert('Win button was not found after 10 minutes', tg_bot)
        location = ag.locateCenterOnScreen('samples\\location.png')
        if location is None:
            abort_with_alert('Location button button was not found', tg_bot)
        ag.click(location.x, location.y)

        first_iter = False
