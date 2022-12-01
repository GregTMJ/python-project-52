from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

VALIDATED_STATUSES = ['new', 'on going', 'testing', 'completed']


def validate_status_naming(status: str):
    """
    validating status by having a list of statuses
    :param status: the name that needs to be created
    """
    if status not in VALIDATED_STATUSES:
        raise ValidationError(
            _('%(name)s is not in a valid status'),
            params={'status': status}
        )
