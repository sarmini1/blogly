from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyViewTestCase(TestCase):
    """test routes for blogly"""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name='Whiskey', last_name="Dog")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

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