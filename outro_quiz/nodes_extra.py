from otree.templating.template import Template
from otree.templating.nodes import Node, register, Expression, smart_split, errors
from wtforms import fields as wtfields  # adjust import if different in your tree
from otree.forms.fields import CheckboxField  # optional; used only for class switch

@register('likertfield')
class LikertFieldNode(Node):
    """
    Usage:
      {% likertfield 'q15' %}
      {% likertfield 'q15' label='<strong>Question with HTML</strong>' %}
      {% likertfield form_field %}
    """
    def process_token(self, token):
        args = smart_split(token.text)[1:]
        if len(args) == 0:
            raise errors.TemplateSyntaxError('likertfield tag requires the name of the field', token)

        # 1st arg: field name or field object
        self.field_expr = Expression(args[0], token)

        # optional label=...
        self.label_expr = None
        for a in args[1:]:
            if a.startswith('label='):
                self.label_expr = Expression(a[len('label='):], token)
            else:
                raise errors.TemplateSyntaxError(f"Unknown argument to likertfield: {a}", token)

    def _resolve_field(self, context):
        arg0 = self.field_expr.eval(context)
        if isinstance(arg0, str):
            if arg0 not in context['form']:
                raise ValueError(f'Field not found in form: {arg0:.20}')
            return context['form'][arg0]
        elif isinstance(arg0, wtfields.Field):
            return arg0
        else:
            raise TypeError(
                "likertfield argument should be a string or Field, e.g. {% likertfield 'q15' %}"
            )

    def wrender(self, context):
        fld = self._resolve_field(context)

        # pick label: explicit override or field's own label text
        label = self.label_expr.eval(context) if self.label_expr else fld.label.text

        # Build the HTML for inputs & labels. Iterating a RadioField yields subfields.
        inputs_html = []
        labels_html = []
        idx = 0
        for sub in fld:
            # sub renders an <input type="radio" ...> when cast to str/called
            input_html = str(sub)
            # label text as raw HTML (allows <strong>, <em>, etc.)
            label_text = getattr(sub.label, 'text', str(sub.label))

            inputs_html.append(f'<td style="">{input_html}</td>')
            labels_html.append(
                f'<td style="vertical-align: top; overflow: visible; white-space: nowrap; text-wrap: wrap;">{label_text}</td>'
            )
            idx += 1

        # Fallback if field is not iterable (e.g., not a RadioField)
        if not inputs_html:
            inputs_html.append(f'<td>{str(fld)}</td>')
            labels_html.append('<td></td>')

        classes = 'mb-3 _formfield'
        if isinstance(fld, CheckboxField):
            classes = 'form-check'
        if fld.errors:
            classes += ' has-errors'

        # Return a raw HTML string; Template here is just for small substitutions.
        return Template(
            '''
<div class="{{classes}}">
  <div class="question">{{label}}</div>
  <table style="table-layout: fixed; min-width: 55rem; width: min-content;">
    <tr>{{ inputs_row }}</tr>
    <tr>{{ labels_row }}</tr>
  </table>
  {% if errors %}
    <div class="form-control-errors">
      {% for e in errors %}{{ e }}<br/>{% endfor %}
    </div>
  {% endif %}
</div>
            '''
        ).render(
            dict(
                classes=classes,
                label=label,  # **left as raw text; engine does not re-escape**
                inputs_row=''.join(inputs_html),
                labels_row=''.join(labels_html),
                errors=fld.errors,
            ),
            strict_mode=True,
        )
