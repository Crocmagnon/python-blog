from django import forms

from articles.models import Comment


class CommentForm(forms.ModelForm):
    required_css_class = "required"
    error_css_class = "error"

    class Meta:
        model = Comment
        fields = ["username", "email", "content"]

    def as_table(self):
        "Return this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row="<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td></tr>",
            error_row=(
                '<tr class="error nonfield"><td colspan="2">%s</td></tr>'
                '<tr class="spacer"><td colspan="2"></td></tr>'
            ),
            row_ender="</td></tr>",
            help_text_html='<br><span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )

    def __init__(self, *args, **kwargs):
        defaults = {
            "label_suffix": "",
        }
        defaults.update(kwargs)

        super().__init__(*args, **defaults)
