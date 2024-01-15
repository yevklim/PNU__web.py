from flask import url_for

from app import db
from app.todo.models import ToDo
from app.todo.forms import ToDoForm
from .base import BaseTest

class TodoTest(BaseTest):

    def test_todo_list(self):
        """Verifies the visibility and correctness of the To-do List view."""
        todos = [
            ToDo(task='Task 1', description='Description 1', completed=False),
            ToDo(task='Task 2', description='Description 2', completed=False),
        ]
        db.session.add_all(todos)
        db.session.commit()
        with self.client:
            response = self.client.get(url_for('todo.list'), follow_redirects=True)

            self.assert200(response)
            self.assertTrue(todos[0].task in response.text, 'Task #1 was not found in the list.')
            self.assertTrue(todos[0].description in response.text, 'Task #1 description was not found in the list.')
            self.assertTrue(todos[1].task in response.text, 'Task #2 was not found in the list.')
            self.assertTrue(todos[1].description in response.text, 'Task #2 description was not found in the list.')

    def test_todo_add(self):
        """Verifies To-do Add functionality."""
        with self.client:
            form = ToDoForm(task='Task 1', description='Description 1')
            response = self.client.post(url_for('todo.add'),
                                        data=form.data,
                                        follow_redirects=True)

            self.assert200(response)
            todo = ToDo.query.first_or_404('Todo item not found.')
            self.assertEqual(todo.task, form.task.data, "Task title doesn't match.")
            self.assertEqual(todo.description, form.description.data, "Task description doesn't match.")

    def test_todo_update(self):
        """Verifies To-do Update functionality."""
        todo = ToDo(task='Task 1', description='Description 1', completed=False)
        db.session.add(todo)
        db.session.commit()
        with self.client:
            response = self.client.get(url_for('todo.update', todo_id=todo.id), follow_redirects=True)

            self.assert200(response)
            self.assertTrue(todo.completed, "Task status was not updated.")

    def test_todo_delete(self):
        """Verifies To-do Delete functionality."""
        todo = ToDo(task='Task 1', description='Description 1', completed=True)
        db.session.add(todo)
        db.session.commit()
        with self.client:
            response = self.client.get(url_for('todo.delete', todo_id=todo.id), follow_redirects=True)

            self.assert200(response)
            todo = ToDo.query.filter_by(id=todo.id).first()
            self.assertIsNone(todo, 'Todo was not deleted.')
