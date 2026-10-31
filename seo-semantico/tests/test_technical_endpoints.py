import unittest
from unittest.mock import patch
from io import BytesIO
from technical_endpoints import check

class Response:
 status=200
 url="https://arquindex.com.br/robots.txt"
 headers={"Content-Type":"text/plain"}
 def __init__(self,data):self.data=data
 def read(self,max_size):return self.data[:max_size]
 def __enter__(self):return self
 def __exit__(self,*args):return False

class EndpointTests(unittest.TestCase):
 def test_robots_sitemaps(self):
  with patch("urllib.request.urlopen",return_value=Response(b"User-agent: *\nAllow: /\nSitemap: https://arquindex.com.br/sitemap.xml")):
   r=check("https://arquindex.com.br/robots.txt")
  self.assertEqual(r["sitemaps"],["https://arquindex.com.br/sitemap.xml"])
 def test_invalid_xml(self):
  with patch("urllib.request.urlopen",return_value=Response(b"<bad")):
   r=check("https://arquindex.com.br/sitemap.xml")
  self.assertIn("error",r)
if __name__=="__main__":unittest.main()
