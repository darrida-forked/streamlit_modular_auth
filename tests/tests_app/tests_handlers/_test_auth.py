class CustomAuthTest:
    def check_credentials(self, username, password):
        if username == "custom_auth_user" and password == "custom_auth_pass":  # nosec
            return True
        return False
