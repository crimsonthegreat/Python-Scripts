# 9.10
from restaraunt import Restaurant

restaraunt = Restaurant("jackie chan's", "chinese")
restaraunt.describe_restaurant()

# 9.11
from user import User
from admin_privileges import Admin

print("\nThe regular user is:")
user = User("joe", "blow")
user.describe_user()
print("\nThe addmin user is:")
admin = Admin("billy", "bob")
admin.describe_user()
admin.privileges.show_privileges()