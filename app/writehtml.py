f = open('temporary.html','w')

message = """<html>
<head></head>
<body><p>""" {{ mylist[0]['title'] }} """</p></body>
</html>"""

f.write(message)
f.close()