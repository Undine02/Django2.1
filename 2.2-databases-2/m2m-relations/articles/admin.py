from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0

        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data['is_main']:
                    count += 1
                elif form.cleaned_data['is_main'] is False:
                    continue

        if count > 1:
            raise ValidationError('Основным может быть только один раздел')
        elif count == 0:
            raise ValidationError('Укажите тег новости')

        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']