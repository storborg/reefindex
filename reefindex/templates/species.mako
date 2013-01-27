<%inherit file="base.mako"/>


<%def name="title()">${species.name}</%def>


<div style="float:right">
  <a href="${request.route_url('edit_species', id=request.matchdict['id'])}">Edit</a>
</div>

<h1>${species.name}</h1>

<h2>
  <em>
    ${species.order_latin} &rarr;
    ${species.family_latin} &rarr;
    ${species.genus_latin} &rarr;
    ${h.abbreviate_latin(species.latin)}
  </em>
</h2>

<dl>
  % if species.size_max:
    <dt>Size Range</dt>
    % if species.size_min and species.size_max:
      <dd>${species.size_min} to ${species.size_max} cm.</dd>
    % elif species.size_max:
      <dd>Up to ${species.size_max} cm.</dd>
    % endif
  % endif
</dl>


<%def name="section(title, contents)">
  % if contents:
    <h3>${title}</h3>
    <p>${contents}</p>
  % endif
</%def>


${self.section('Description', species.description)}
${self.section('Range', species.range)}
${self.section('Diet', species.diet)}
${self.section('Breeding', species.breeding)}
${self.section('Ethics', species.ethics)}
