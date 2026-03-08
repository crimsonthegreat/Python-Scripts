# 8.15
import printing_functions

unprinted_designs = ['chess piece', 'drawer handle', 'cap']
completed_models = []

printing_functions.print_models(unprinted_designs, completed_models)
printing_functions.show_completed_models(completed_models)

# 8.16
import user_profile_functions

user_profile = user_profile_functions.build_profile('crimson', 'thgreat',
                                                    location='phoenix')
print(user_profile)

from user_profile_functions import build_profile

user_profile = build_profile('crimson', 'thgreat', location='phoenix')
print(user_profile)

from user_profile_functions import build_profile as bp

user_profile = bp('crimson', 'thgreat', location='phoenix')
print(user_profile)

import user_profile_functions as up

user_profile = up.build_profile('crimson', 'thgreat', location='phoenix')
print(user_profile)

from user_profile_functions import *

user_profile = user_profile_functions.build_profile('crimson', 'thgreat',
                                                    location='phoenix')
print(user_profile)