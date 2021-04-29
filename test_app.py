from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyViewTestCase(TestCase): #could be helpful to separate test case classes
    """test routes for blogly"""

    def setUp(self):
        """Add sample user."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name='Whiskey', last_name="Dog")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        post = Post(title="test_post", content="testing123", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users_redirect(self):
        """redirect status received"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")

    def test_users_redirection_followed(self):
        """redirects to correct page"""
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('user page for testing', html)  

    def test_users_html(self):
        """renders user list html"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('user page for testing', html)               

    def test_display_add_user_form(self):
        """renders add user form html"""
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('add user form for testing', html)

    def test_users_add_form_submit_redirect(self):
        """test add form submit redirect"""
        with app.test_client() as client:
            resp = client.post("/users/new", 
                                data = {'first_name': 'Henry', 
                                        'last_name': 'Pennyworth',
                                        'image_url':''})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users") 

    def test_users_add_form_submit_followed(self):
        """test add form submit redirect followed html"""
        with app.test_client() as client:
            resp = client.post("/users/new", 
                                data = {'first_name': 'Henry', 
                                        'last_name': 'Pennyworth',
                                        'image_url':''}, 
                                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Henry', html)                         

    def test_users_delete_submit_redirect(self):
        """test delete submit redirect"""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")

    def test_users_delete_submit_redirect_followed(self):
        """test delete submit redirect"""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Whiskey', html)
    
    def test_display_add_new_post_form(self):
        """test display of new post form"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)
        
            self.assertEqual(resp.status_code, 200)
            self.assertIn('add post form for testing', html)

    def test_add_new_post_from_form_redirect(self):
        """test adding new post"""
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new',
                                data = {'title': 'test_post', #rename to something more specific, like test title 1, etc
                                'content': 'asl;kdf', #same as above
                                'user_id':self.user_id})
        
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"http://localhost/users/{self.user_id}")
    
    def test_add_new_post_redirect_followed(self):
        """test add post redirect"""
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new',
                                data = {'title': 'test_post',
                                'content': 'asl;kdf',
                                'user_id':self.user_id},
                                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_post', html)
    
    def test_show_post_detail_page(self):
        """test showing a post detail page"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)
        
            self.assertEqual(resp.status_code, 200)
            self.assertIn('displays post page', html)
            #add assert that specific phrase in the content itself appears
    
    def test_delete_post_redirect(self):
        """tests deleting a post redirect happens"""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"http://localhost/users/{self.user_id}")

    def test_delete_post_redirect_followed(self):
        """tests deleting a post redirect followed"""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete',
                                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('test_post', html)

    def test_show_edit_post_form(self):
        """test showing edit post form"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)
        
            self.assertEqual(resp.status_code, 200)
            self.assertIn('edit post form for testing', html)

    def test_editing_post_redirect(self):
        """tests editing a post redirect happens"""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit',
                                data={'title': 'test_post_edited',
                                'content': 'asl;kdf_edited'})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"http://localhost/posts/{self.post_id}")

    def test_edit_post_redirect_followed(self):
        """tests editing a post redirect followed"""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit',
                                data={'title': 'test_post_edited',
                                'content': 'asl;kdf_edited'},
                                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_post_edited', html)