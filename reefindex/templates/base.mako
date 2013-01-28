<!DOCTYPE html>
<html>
  <head>
    <title>${self.title()}</title>
    <link rel="stylesheet" href="${request.static_url('reefindex:static/css/style.css')}">
  </head>
  <body>
    <div class="header">
      ${self.search_form()}
      <a href="/">Reef Index</a>
    </div>
    <div class="main">
      ${next.body()}
    </div>
  </body>
</html>


<%def name="search_form()">
  <form action="${request.route_url('search')}" method="get">
    <input class="input-mini" type="text" name="size_lower" value="${request.params.get('size_lower', '')}" placeholder="Min Size">
    <input class="input-mini" type="text" name="size_upper" value="${request.params.get('size_upper', '')}" placeholder="Max Size">
    <input class="input-medium" type="text" name="q" value="${request.params.get('q', '')}" placeholder="Keywords">
    <button type="submit">Search</button>
  </form>
</%def>


<%def name="title()"></%def>
