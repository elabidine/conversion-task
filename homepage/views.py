from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

content = """
<html>
    <head>
         <title>FlexUp</title>

    </head>
    <body>
      <h1>Welcome to FlexUp</h1>
  <p>
    Welcome to Flexup, an app by
    <em>Cosys</em>!
  </p>
    </body>
</html>
"""


def home_page(request):
    """"""
    return HttpResponse(content)
