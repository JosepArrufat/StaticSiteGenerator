import unittest
import textwrap
from generate_page import extract_title

class TestFindH1(unittest.TestCase):
    def test_find_header(self):
        md = textwrap.dedent("""
        > This is a quote block.
        # This is an h1
        > And can also include **inline** formatting.
        """)
        h1 = extract_title(md)
        self.assertEqual(h1, "This is an h1")
    def test_headings(self):
        md = textwrap.dedent("""
        ## This is an H2
        ### This is an H3
        #### This is an H4
         # This is an H1
        ##### This is an H5
        ###### This is an H6
        """)
        h1 = extract_title(md)
        self.assertEqual(h1, "This is an H1")
    

if __name__ == "__main__":
    unittest.main()
