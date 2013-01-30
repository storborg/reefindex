<!DOCTYPE html>
<html>
  <head>
    <title>${self.title()}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <link rel="stylesheet" href="${request.static_url('reefindex:static/css/style.css')}">
  </head>
  <body>
    <div class="header">
      <a href="/">Reef Index</a>
      ${self.search_form()}
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
