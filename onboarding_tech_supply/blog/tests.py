from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post

# Create your tests here.

class PostListTests(APITestCase):
    def test_add_post(self):
        url = reverse('post-list')
        data = {'title': 'Lorem Ipsum test', 'content': 'Lorem ipsum dolor sit amet'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Lorem Ipsum test')
    
    def test_add_invalid_post(self):
        url = reverse('post-list')
        data = {'content': 'Lorem ipsum dolor sit amet'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class UpdateAutorTests(APITestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Lorem Ipsum test', content='Lorem ipsum dolor sit amet', autor='Old Author')

    def test_update_autor(self):
        url = reverse('update-autor', kwargs={'post_id': self.post.id})
        new_autor = 'New Author'

        data = {'autor': new_autor}
        response = self.client.patch(url,data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.post.refresh_from_db()
        self.assertEqual(self.post.autor, new_autor)
    
    def test_update_author_invalid_post(self):
        url = reverse('update-autor', kwargs={'post_id': 999})  # Invalid id

        data = {'autor': 'New Author'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)