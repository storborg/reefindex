<%inherit file="base.mako"/>


<%def name="title()">Search Results</%def>


<%def name="species(result)">
  <div class="species">
    <h2>
      <a href="${request.route_url('species', id=result._id)}">${result.name}</a>
      <em>${result.latin}</em>
    </h2>
    <p>${result.description}</p>
  </div>
</%def>


<div style="float:right">
  ${page.pager()}
</div>


% for result in page:
  ${self.species(result)}
% endfor
% if len(page) == 0:
  <p>No results.</p>
% endif
