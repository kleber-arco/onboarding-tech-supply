from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post

# Create your tests here.

class PostListTests(APITestCase):
    def test_list_posts_descending_order(self):
        self.post1 = Post.objects.create(title='Post 1', content='Content of post 1')
        self.post2 = Post.objects.create(title='Post 2', content='Content of post 2')
        self.post3 = Post.objects.create(title='Post 3', content='Content of post 3')

        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify if posts are returned in correct order
        posts = response.data
        self.assertEqual(len(posts), 3)
        self.assertEqual(posts[0]['title'], 'Post 3')  # Most recent
        self.assertEqual(posts[1]['title'], 'Post 2')
        self.assertEqual(posts[2]['title'], 'Post 1')  # Oldest

        self.post1.delete()
        self.post2.delete()
        self.post3.delete()

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