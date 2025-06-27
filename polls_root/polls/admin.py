from django.contrib import admin

from . import models
from utils.admin import small_text_input_mixin


SmallTextInputMixin = small_text_input_mixin(50)


@admin.register(models.Option)
class OptionAdmin(SmallTextInputMixin, admin.ModelAdmin):
    list_display = ('question', 'text', 'votes')
    fields = ('question', 'text')
    list_display_links = ('text', )


class OptionInline(SmallTextInputMixin, admin.TabularInline):
    model = models.Option
    fields = OptionAdmin.fields


@admin.register(models.Question)
class QuestionAdmin(SmallTextInputMixin, admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'views', 'votes')
    inlines = (OptionInline, )
    fields = ('title', 'pub_date')
