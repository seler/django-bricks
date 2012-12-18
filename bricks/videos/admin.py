# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings

from .models import Video, ConvertedVideo
#from .forms import VideoForm
#from django.conf.urls import patterns
#from django.shortcuts import render_to_response
#from django.db import models
#from django import forms
#from django.utils.html import escape, conditional_escape
#from django.utils.encoding import force_unicode
#from django.utils.safestring import mark_safe
#from django.forms.util import flatatt
#from django.forms.widgets import CheckboxInput, FILE_INPUT_CONTRADICTION
from django.core.files.storage import get_storage_class
from bricks.admin import PageInlineAdmin
from bricks.collections.admin import CollectionObjectInlineAdmin


safe_storage = get_storage_class(settings.DEFAULT_FILE_STORAGE)()


class ConvertedVideoInlineAdmin(admin.TabularInline):
    model = ConvertedVideo
    readonly_fields = ('format', 'file')
    #fields = ['url_file',]
    extra = 0
    max_num = 0

"""
class UploadifyInput(forms.ClearableFileInput):
    template_with_initial = u'%(initial_text)s: %(initial)s %(clear_template)s<br />%(input)s'

    def render(self, name, value, attrs=None):
        substitutions = {
        'initial_text': self.initial_text,
        'input_text': self.input_text,
        'clear_template': '',
        'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        if value is None:
            value = ''
            final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
            if value != '':
                # Only add the 'value' attribute if a value is non-empty.
                final_attrs['value'] = force_unicode(self._format_value(value))
                substitutions['input'] = mark_safe(u'<input%s />' % flatatt(final_attrs))

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = (u'<a href="%s">%s</a>' % (escape(value.url), escape(force_unicode(value))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = forms.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = u'<span class="clearable-file-input">%s</span>' % (self.template_with_clear % substitutions,)
                template = u'<p class="file-upload">%s</p>' % template

        return mark_safe(template % substitutions)

    def value_from_datadict(self, data, files, name):
        filename = data.get('file', None)
        upload = None
        if filename:
            upload = safe_storage.open('video/original/%s' % filename)
            if not self.is_required and CheckboxInput().value_from_datadict(
            data, files, self.clear_checkbox_name(name)):
                if upload:
                    # If the user contradicts themselves (uploads a new file AND
                    # checks the "clear" checkbox), we return a unique marker
                    # object that FileField will turn into a ValidationError.
                    return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload
"""

from bricks import USE_TINYMCE
if USE_TINYMCE:
    from tinymce.widgets import TinyMCE

from django import forms


class VideoAdminForm(forms.ModelForm):
    if USE_TINYMCE:
        description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=False)

    class Meta:
        model = Video


class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    inlines = (PageInlineAdmin, ConvertedVideoInlineAdmin, CollectionObjectInlineAdmin)
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title')
    search_fields = ('title',)
    actions = ['force_convert']

    """
    formfield_overrides = {
    models.FileField: {'widget': UploadifyInput},
    }
    """

    def save_model(self, request, obj, form, change, *args, **kwargs):
        if obj.id is None:
            ret = super(VideoAdmin, self).save_model(request, obj, form,
                                                     change, *args, **kwargs)
            obj.process_video()
            return ret
        else:
            return super(VideoAdmin, self).save_model(request, obj, form,
                                                      change, *args, **kwargs)

    def force_convert(self, request, queryset):
        for video in queryset:
            video.ready = False
            video.save()
            video.converted_videos.all().delete()
            video.process_video()
            self.message_user(request, u'Ponowne konwertowanie wybranych filmów.')
    force_convert.short_description = u'Ponowna konwersja filmu'


"""
def save_related(self, request, form, formsets, change):
    super(VideoAdmin, self).save_related(request, form, formsets, change)
    if getattr(self, 'obj', None):
        category = self.obj.get_category()
        if category:
            Video.objects.filter(pk=self.obj.pk).update(category_path=category.slug)
            def get_urls(self):
                urls = super(VideoAdmin, self).get_urls()
                video_urls = patterns('',
                (r'^upload_complete/$', self.upload_complete)
                )
                return video_urls + urls
"""
"""
def upload_complete(self, request):
    return render_to_response('admin/videos/video/upload_complete.html')
"""
"""
def set_ready(self, request, queryset):
    cnt = 0
    for video in queryset:
        video.ready = True
        video.save()
        cnt += 1
        self.message_user(request, u'%s pomyślnie oznaczonych jako skonwertowane.' % cnt)
        set_ready.short_description = u'Oznacz jako skonwertowane'

    def force_convert(self, request, queryset):
        for video in queryset:
            video.ready = False
            video.save()
            video.converted_videos.all().delete()
            video.process_video()
            self.message_user(request, u'Ponowne konwertowanie wybranych filmów.')
            force_convert.short_description = u'Ponowna konwersja filmu'
            def get_duration(self, obj):
                if obj.duration:
                    return str(datetime.timedelta(seconds=obj.duration))
        return 'Nieznany'
    get_duration.short_description = 'Czas trwania'

"""

admin.site.register(Video, VideoAdmin)
admin.site.register(ConvertedVideo)
