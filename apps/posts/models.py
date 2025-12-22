from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta
from helper import linkedin

User = settings.AUTH_USER_MODEL  # "auth.User"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    share_now = models.BooleanField(default=None, null=True, blank=True)
    share_at = models.DateTimeField(null=True, blank=True)

    share_start_at = models.DateTimeField(null=True, blank=True)
    share_complete_at = models.DateTimeField(null=True, blank=True)

    share_on_linkedin = models.BooleanField(default=False)
    shared_at_linkedin = models.DateTimeField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.share_now is None and self.share_at is None:
            raise ValidationError({
                "share_at": "You must select a time to share or share it now",
                "share_now": "You must select a time to share or share it now",
            })

        if self.share_on_linkedin:
            self.verify_can_share_on_linkedin()

    def get_scheduled_platforms(self):
        platforms = []
        if self.share_on_linkedin:
            platforms.append("linkedin")
        return platforms

    def save(self, *args, **kwargs):
        # Pre-save logic
        if self.share_now:
            self.share_at = timezone.now()

        super().save(*args, **kwargs)
        # Post-save logic removed (Inngest)

    def perform_share_on_linkedin(self, mock=False, save=False):
        if self.shared_at_linkedin:
            return self

        if not mock:
            try:
                linkedin.post_to_linkedin(self.user, self.content)
            except Exception:
                raise ValidationError({
                    "content": "Could not share to LinkedIn."
                })

        self.shared_at_linkedin = timezone.now()

        if save:
            self.save(update_fields=["shared_at_linkedin"])

        return self

    def verify_can_share_on_linkedin(self):
        if len(self.content) < 5:
            raise ValidationError({
                "content": "Content must be at least 5 characters long."
            })

        if self.shared_at_linkedin:
            raise ValidationError({
                "share_on_linkedin": f"Content was already shared on LinkedIn at {self.shared_at_linkedin}.",
                "content": "Content is already shared on LinkedIn."
            })

        try:
            linkedin.get_linkedin_user_details(self.user)
        except linkedin.UserNotConnectedLinkedIn:
            raise ValidationError({
                "user": "You must connect LinkedIn before sharing."
            })
        except Exception as e:
            raise ValidationError({
                "user": str(e)
            })
