# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import subprocess
import requests as rq
import time

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

# TODO: Change "Template" to a unique name for your skill
class UpdateSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(UpdateSkill, self).__init__(name="UpdateSkill")
        
        # Initialize working variables used within the skill.
        self.count = 0

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("").require("Update").require("Self"))
    def handle_hello_world_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        self.speak('Looking for updates.')

        def main(user_name):

            """Simple program that lists USER_NAME Github repositories."""

            num = 0
            repo_list = list()

            # Loop for pagination: iterate over every page and store repository names
            while True:

                GitURL = 'https://api.github.com/users/{}/repos?page={}'.format(user_name, num)
                r = rq.get(GitURL)

                try:
                    repo_list = repo_list + [dc['name'] for dc in r.json()]
                except:
                    # API daily limit exceeded
                    print('\n', r, '\n', r.json()['message'])
                    exit()
                    break

                if len(r.json()) == 0:
                    break

                num += 1

            repo_num = len(set(repo_list))
            print('Number of repos: {}\n'.format(repo_num))

            for repo in set(repo_list):
                subprocess.call('msm update ' + repo + '.' + user_name, shell=True)

        main('drewlg')


        self.speak('Update complete.')
        # Wait for 5 seconds
        time.sleep(5)
        self.speak('Rebooting.')
        subprocess.call('sudo reboot', shell=True)
    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return UpdateSkill()

