from datetime import timezone
from django.db import models
from ResetPassword.utils import generate_token

from User.models import User

class ResetPasswordToken(models.Model):
    class Meta:
        verbose_name = "Password Reset Token"
        verbose_name_plural = "Password Reset Tokens"

    id = models.AutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        related_name='password_reset_tokens',
        on_delete=models.CASCADE,
        verbose_name="The User which is associated to this password reset token"
    )

    expiration_date = models.DateTimeField(
        verbose_name="When was this token generated"
    )

    reset_token = models.CharField(
        "Reset token",
        max_length=64,
        db_index=True,
        unique=True
    )

    tries_counter = models.IntegerField(
        default=0,
        verbose_name="Number of tries with this token"
    )

    """def save(self, *args, **kwargs):
        if not self.reset_token:
            self.reset_token = generate_token(self.user.email)
        return super(ResetPasswordToken, self).save(*args, **kwargs)"""
    
    def get_or_create(user):
        token = ResetPasswordToken.objects.filter(user=user)
        if token is None:
            reset_passowrd_token = ResetPasswordToken.objects.create(
                user=user,
                expiration_date=timezone.now() + timezone.timedelta(minutes=15),
                reset_token=generate_token(user.email)
            )
            return reset_passowrd_token
        else:
            token.expiration_date=timezone.now() + timezone.timedelta(minutes=15)
            token.save()
            return token
        

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)
    
    def increment_tries(self, max_tries=4):
        if self.tries_counter >= max_tries:
            self.user.set_temporarily_inactive()
            self.delete()
        else:
            self.tries_counter += 1
            self.save()
    
    @staticmethod
    def delete_tokens_espired():
        ResetPasswordToken.objects.filter(expiration_date__lt=timezone.now()).delete()
        """for token in tokens:
            if timezone.now() > token.expiration_date:
                token.delete()"""