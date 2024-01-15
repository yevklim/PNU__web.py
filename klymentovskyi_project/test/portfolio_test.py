from flask import url_for
from .base import BaseTest

class PortfolioTest(BaseTest):

    def test_main_view(self):
        """Verifies the visibility of the Main view."""
        with self.client:
            response = self.client.get(url_for('portfolio.main'))
            self.assert200(response)
            self.assertIn('Main', response.text)
            self.assertIn('Laetamur quaerendo', response.text)

    def test_projects_view(self):
        """Verifies the visibility of the Projects view."""
        with self.client:
            response = self.client.get(url_for('portfolio.projects'))
            self.assert200(response)
            self.assertIn('Big Projects', response.text)
            self.assertIn('Project Alpha', response.text)

    def test_skills_view(self):
        """Verifies the visibility of the Skills view."""
        with self.client:
            response = self.client.get(url_for('portfolio.skills'))
            self.assert200(response)
            self.assertIn('Professional Skills', response.text)
            self.assertIn('Desktop Application Development', response.text)

    def test_skill_view(self):
        """Verifies the visibility of the Skill #2 view."""
        with self.client:
            response = self.client.get(url_for('portfolio.skills', idx=2))
            self.assert200(response)
            self.assertIn('Skill #2: Desktop Application Development', response.text)
            self.assertIn('Subskills', response.text)

    def test_about_view(self):
        """Verifies the visibility of the About Me view."""
        with self.client:
            response = self.client.get(url_for('portfolio.about'))
            self.assert200(response)
            self.assertIn('About me', response.text)
            self.assertIn('Itinera Alexandri', response.text)
