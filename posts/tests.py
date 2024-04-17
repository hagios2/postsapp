from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status
from .views import PostList
from django.contrib.auth import get_user_model

User = get_user_model()


class PostListAPITestCase(APITestCase):
    def setUp(self):
        #either use api request factory or the test client
        self.url = reverse('post_list')

    #     self.factory = APIRequestFactory()
    #     self.view = PostList.as_view()
    #     self.user = User.objects.create(
    #         email='prince@gmail.com',
    #         password='password',
    #         username='prince',
    #     )

    def authenticate_user(self):
        self.client.post(reverse('signup'), {'username': 'johndoe', 'password': 'password', 'email': 'test@gmail.com'})
        response = self.client.post(reverse('login'), {'email': 'test@gmail.com', 'password': 'password'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['tokens']['access'])

    def test_list_posts(self):
        # either use api request factory or the test client
        response = self.client.get(self.url)

        # request = self.factory.get(self.url)
        # response = self.view(request)
        self.assertEqual(response.data['message'], 'fetched posts')
        self.assertEqual(response.data['data'], [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        self.authenticate_user()
        sample_post = {
            'content': 'this is a test content',
            'title': 'test title',
        }

        response = self.client.post(self.url, sample_post)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'post created successfully')
        self.assertEqual(response.data['data']['title'], sample_post['title'])
        self.assertEqual(response.data['data']['content'], sample_post['content'])
