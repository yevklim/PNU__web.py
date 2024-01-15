from flask import url_for
from flask_login import current_user, login_user

from app.user.models import User
from app.user.forms import RegistrationForm, LoginForm, UpdateAccountForm
from .base import BaseTest

class UserTest(BaseTest):

    def test_register_view(self):
        """Verifies the visibility of the Register view."""
        with self.client:
            response = self.client.get(url_for('user.register'))

            self.assert200(response)
            self.assertTrue("SIGN UP" in response.text, 'Menu item "SIGN UP" is not found in the menu.')
            self.assertTrue("Username" in response.text, 'Form field "Username" is not found on the form.')
            self.assertTrue("Password" in response.text, 'Form field "Password" is not found on the form.')
            self.assertTrue("Sign Up" in response.text, 'Form submit button "Sign Up" is not found on the form.')

    def test_register_post(self):
        """Verifies registration form submittion."""
        with self.client:
            form = RegistrationForm(data=dict(username='test2', email='test2@test.com', password='testpass', confirm_password='testpass'))
            response = self.client.post(
                url_for('user.register'),
                data=form.data,
                follow_redirects=True
            )

            self.assert200(response)
            self.assertTrue("Account created for test2" in response.text, 'Success flash message is not found in the page.')

            user = User.query.filter_by(email=form.email.data).first()
            self.assertIsNotNone(user, 'User not found in the database.')
            self.assertEqual(user.username, form.username.data, "Username doesn't match.")

    def test_login_view(self):
        """Verifies the visibility of the Login view."""
        with self.client:
            response = self.client.get(url_for('user.login'))

            self.assert200(response)
            self.assertTrue("SIGN IN" in response.text, 'Menu item "SIGN IN" is not found in the menu.')
            self.assertTrue("E-mail" in response.text, 'Form field "E-mail" is not found on the form.')
            self.assertTrue("Password" in response.text, 'Form field "Password" is not found on the form.')
            self.assertTrue("Remember Me" in response.text, 'Form field "Remember me" is not found on the form.')
            self.assertTrue("Sign In" in response.text, 'Form submit button "Sign In" is not found on the form.')

    def test_login_post(self):
        """Verifies authentication form submittion."""
        with self.client:
            form = LoginForm(data=dict(email='test@test.com', password='testpass'))
            response = self.client.post(
                url_for('user.login'),
                data=form.data,
                follow_redirects=True
            )

            self.assert200(response)
            self.assertTrue('Successfully signed in' in response.text, 'Success flash message is not found in the page.')
            self.assertFalse('Incorrect e-mail or password' in response.text, 'Failure flash message is found in the page.')
            self.assertTrue(current_user.is_authenticated, 'User is not authenticated.')
            self.assertEqual(current_user.email, form.email.data, "E-mail doesn't match.")

    def test_logout_post(self):
        """Verifies logout functionality."""
        with self.client:
            login_user(User.query.first_or_404('User not found.'))

            response = self.client.get(url_for('user.logout'), follow_redirects=True)

            self.assert200(response)
            self.assertTrue('You have signed out' in response.text, 'Success flash message is not found in the page.')
            self.assertFalse(current_user.is_authenticated)

            self.assertTrue("SIGN IN" in response.text, 'Menu item "SIGN IN" is not found in the menu.')
            self.assertTrue("E-mail" in response.text, 'Form field "E-mail" is not found on the form.')
            self.assertTrue("Password" in response.text, 'Form field "Password" is not found on the form.')
            self.assertTrue("Remember Me" in response.text, 'Form field "Remember me" is not found on the form.')
            self.assertTrue("Sign In" in response.text, 'Form submit button "Sign In" is not found on the form.')

    def test_update_account_post(self):
        """Verifies account update form submittion."""
        user = User.query.first_or_404('User not found.')
        with self.client:
            login_user(user)

            form = UpdateAccountForm(data=dict(username='Foobar', email='foobar@foo.bar'))
            response = self.client.post(
                url_for('user.account', action='update_profile'),
                data = form.data,
                follow_redirects=True
            )

            self.assert200(response)
            self.assertEqual(user.username, form.username.data, "Username was not updated.")
            self.assertEqual(user.email, form.email.data, "E-mail was not updated.")
