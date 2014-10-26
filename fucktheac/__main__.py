"""Program entry point!"""
from config import CONFIG
import pychromecast
from ouimeaux.environment import Environment
from ouimeaux.signals import receiver, statechange

cast = pychromecast.get_chromecast(friendly_name=CONFIG['cast_name'])
print("Connected to chromecast {}".format(cast))

env = Environment()
env.start()
env.discover(5)
switch = env.get_switch(CONFIG['wemo_name'])
print("Connected to switch {}".format(switch))


@receiver(statechange, sender=switch)
def volume_event(**kwargs):
    """Handles volume control based on wemo on/off events"""
    notches = CONFIG['notches']
    if kwargs['state'] == 1:
        for _ in range(notches):
            print("TURN DOWN FOR WHAT!")
            cast.volume_up()
    elif kwargs['state'] == 8:
        for _ in range(notches):
            print("OKAY MOM!")
            cast.volume_down()


if __name__ == '__main__':
    env.wait()
