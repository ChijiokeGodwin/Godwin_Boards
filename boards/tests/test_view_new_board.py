from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..views import new_board
from ..models import Board
from ..forms import NewBoardForm

# Create your tests here.

class NewBoardTests(TestCase) :
    def setUp(self) :
        User.objects.create_user(username = 'john', email = 'john@doe.com', password = '123')
        self.client.login(username = 'john', password = '123')

    def test_new_board_view_success_status_code(self) :
        response = self.client.get(reverse('new_board'))
        self.assertEquals(response.status_code, 200)

    def test_new_board_url_resolves_new_board_view (self) :
        view = resolve ('/board/new/')
        self.assertEquals(view.func, new_board)

    def test_new_board_view_contains_link_back_to_home_view(self) :
        response = self.client.get(reverse('new_board'))
        home_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(home_url))

    def test_csrf(self) :
        response = self.client.get(reverse('new_board'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_board_valid_post_data(self):
        url = reverse('new_board')
        data = {
            'name':'Lorem',
            'description':'Lorem ipsum'}
        response = self.client.post(url, data)
        self.assertTrue(Board.objects.exists())

    def test_new_board_invalid_post_data(self) :
        url = reverse('new_board')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEquals (response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self) :
        url = reverse('new_board')
        data = {
            'name': '', 'description': ''}
        response = self.client.post(url, data)
        self.assertFalse (Board.objects.exists())
        self.assertEquals (response.status_code, 200)

    def test_contains_form(self) :
        url = reverse('new_board')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewBoardForm)
    

