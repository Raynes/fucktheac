import time
from config import CONFIG
import pychromecast
from ouimeaux.environment import Environment
from ouimeaux.signals import receiver, statechange

cast = None


def reset_chromecast():
    """Reset the chromecast connection."""
    global cast
    cast = pychromecast.get_chromecast(friendly_name=CONFIG['cast_name'])
    print("Connected to chromecast {}".format(cast))
    time.sleep(3)

env = Environment()
env.start()
env.discover(5)
switch = env.get_switch(CONFIG['wemo_name'])
print("Connected to switch {}".format(switch))

reset_chromecast()


def safe_volume_toggle(direction, notches):
    try:
        if direction == 1:
            for _ in notches:
                print("TURN DOWN FOR WHAT!")
                cast.volume_up()
        elif direction == 8:
            for _ in notches:
                print("OKAY MOM!")
                cast.volume_down()
    except Exception:
        print("Oh noes, think we lost connection to the chromecast."
              "Give me a moment and I'll fix er up...")
        reset_chromecast()
        safe_volume_toggle(direction, notches)


@receiver(statechange, sender=switch)
def volume_event(**kwargs):
    """Handles volume control based on wemo on/off events"""
    notches = CONFIG['notches']
    safe_volume_toggle(kwargs['state'], range(notches))

if __name__ == '__main__':
    env.wait()
