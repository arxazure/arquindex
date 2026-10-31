import unittest
from semantic_block_injector import inject

class InjectorTests(unittest.TestCase):
    def test_preserves_outside_markup(self):
        original='<h1>Original</h1><!-- ARQ-SEMANTIC:demo:START -->antigo<!-- ARQ-SEMANTIC:demo:END --><footer>Rodapé</footer>'
        result=inject(original,"demo",{"title":"Novo","paragraphs":["Texto"]})
        self.assertIn("<h1>Original</h1>",result)
        self.assertIn("<footer>Rodapé</footer>",result)
        self.assertIn("<h2>Novo</h2>",result)
    def test_rejects_missing_markers(self):
        with self.assertRaises(ValueError):inject("<html></html>","demo",{"title":"Novo"})
    def test_escapes_html(self):
        result=inject("<!-- ARQ-SEMANTIC:demo:START --><!-- ARQ-SEMANTIC:demo:END -->","demo",{"title":"<script>x</script>"})
        self.assertNotIn("<script>",result)
if __name__=="__main__":unittest.main()
