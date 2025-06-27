from typing import Type

from django.db import models
from django import forms


def small_text_input_mixin(size: int) -> Type:
    class SmallTextInputMixin:
        formfield_overrides = {
            models.TextField: {
                'widget': forms.TextInput(attrs={'size': size})
            },
        }
    return SmallTextInputMixin
