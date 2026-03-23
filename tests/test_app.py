import unittest 
from app import app 

class CMSTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True 
        self.client = app.test_client()
        

    def test_index(self):
        with self.client.get("/") as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertIn("about.md", response.get_data(as_text=True))
            self.assertIn("changes.txt", response.get_data(as_text=True))
            self.assertIn("history.txt", response.get_data(as_text=True))
        
    def test_viewing_text_document(self):
        with self.client.get("/history.txt") as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/plain; charset=utf-8")
            self.assertIn("Python 0.9.0 (initial release) is released.", response.get_data(as_text=True))
            
    def test_document_not_found(self):
        with self.client.get("/non_existing.txt") as response:
            self.assertEqual(response.status_code, 302)
            
        with self.client.get(response.headers['Location']) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("non_existing.txt does not exist",
                          response.get_data(as_text=True))
        
        with self.client.get("/") as response:
            self.assertNotIn("non_existing.txt does not exist",
                             response.get_data(as_text=True))
            
    def test_viewing_markdown_document(self):
        response = self.client.get("/about.md")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        self.assertIn('<h1>Python is...</h1>', response.get_data(as_text=True))
        
    def test_editing_document(self):
        response = self.client.get("/changes.txt/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<textarea", response.get_data(as_text=True))
        self.assertIn('<button type="submit"', response.get_data(as_text=True))
        
    def test_editing_markdown_document(self):
        response = self.client.post(
            "/changes.txt/edit", 
            data={'file_content': "new content"}
        )
        self.assertEqual(response.status_code, 302)
        
        follow_response = self.client.get(response.headers['Location'])
        self.assertIn("changes.txt has been updated", follow_response.get_data(as_text=True))

        
if __name__ == "__main__":
    unittest.main()