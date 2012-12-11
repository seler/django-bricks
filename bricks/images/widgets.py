from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers


class CropImageFileInput(ClearableFileInput):
    template_with_initial = u"""%(initial_text)s: %(initial)s<br />
    %(clear_template)s %(cropping_template)s<br />
    %(input_text)s: %(input)s"""

    template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    cropping_text = _('Cropping')

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'cropping_text': self.cropping_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            from .image import get_image
            from .models import ResizedImage

            template = self.template_with_initial
            substitutions['initial'] = (u'<a href="%s"><img src="%s" /></a>'
                                        % (escape(value.url),
                                           get_image(value, ResizedImage.MODE_SCALE, 320, 180)))

            changelist_url = urlresolvers.reverse('admin:images_resizedimage_changelist')
            cropping_link = '%s?original_name=%s' % (changelist_url, value.name)

            substitutions['cropping_template'] = (u'<a href="%s">%s</a>'
                                                  % (cropping_link, self.cropping_text))

            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)


class AdminCropImageFileWidget(CropImageFileInput):
    template_with_initial = (u'<p class="file-upload">%s</p>' % CropImageFileInput.template_with_initial)
    template_with_clear = (u'<span class="clearable-file-input">%s</span>' % CropImageFileInput.template_with_clear)
