## Class methods involved in account management:
- check_usr_pass()
- check_unique_email() x
- check_unique_usr() x
- register_new_user()
- check_username_exists()
- check_email_exists()
- change_passwd()
- check_current_passwd() x


## Simplify similar/redundant logic
- merge check_usr_pass() and check_current_passwd()
- merge check_unique_email() and check_email_exists()
- merge check_unique_usr() and check_username_exists()


## Resulting List of methods needed for custom user storage 
- check_password()
- check_email_exists()
- check_user_exists()
- register_new_user()
- change_password()
