

class CustomAuthTest:
    def check_password(self, username, password):
        if username == "custom_auth_user" and password == "custom_auth_pass":
            return True
        return False