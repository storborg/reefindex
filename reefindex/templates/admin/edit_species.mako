<%inherit file="/base.mako"/>

<%namespace name="forms" file="/common/forms.html"/>

<div style="float:right">
  <a href="${request.route_url('species', id=species.id)}">View Entry</a>
</div>

<h1>Edit Species</h1>

<form action="." method="post">
  ${forms.ltext('latin', species.latin)}
  ${forms.ltext('name', species.name)}

  ${forms.ltextarea('description', species.description)}
  ${forms.ltextarea('range', species.range)}
  ${forms.ltextarea('diet', species.diet)}
  ${forms.ltextarea('breeding', species.breeding)}
  ${forms.ltextarea('ethics', species.ethics)}

  ${forms.ltext('size_min', species.size_min)}
  ${forms.ltext('size_max', species.size_max)}
</form>
