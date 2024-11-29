from django.core.exceptions import ValidationError

class SpecialCharacterPasswordValidator:
        def validate(self, password, user=None):
            if not any(char in "!@#$%^&*()" for char in password):
                raise ValidationError(
                    "Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&*()).",
                    code='password_no_special',
                )

        def get_help_text(self):
            return "Votre mot de passe doit contenir au moins un caractère spécial (!@#$%^&*())."