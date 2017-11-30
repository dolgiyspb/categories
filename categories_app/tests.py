from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

# Create your tests here.
from categories_app.models import Category


class CategoriesTestCase(APITestCase):
    def test_get_category(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # make simple relationships c0->(c1->(c2, c3), c4)
        c1 = Category(name='c1')
        c1.save()
        c2 = Category(name='c2')
        c2.save()
        c2.parents.add(c1)
        c2.save()
        c3 = Category(name='c3')
        c3.save()
        c3.parents.add(c1)
        c3.save()
        c0 = Category(name='c0')
        c0.save()
        c1.parents.add(c0)
        c1.save()
        c4 = Category(name='c4')
        c4.save()
        c4.parents.add(c0)
        c4.save()

        url = reverse('category-detail', kwargs={'pk': c1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)
        self.assertIn('parents', response.data)
        self.assertIn('children', response.data)
        self.assertIn('siblings', response.data)
        # check self
        self.assertEqual(response.data['id'], c1.id)
        self.assertEqual(response.data['name'], c1.name)
        # check parents
        self.assertEqual(len(response.data['parents']), 1)
        self.assertEqual(response.data['parents'][0]['id'], c0.id)
        self.assertEqual(response.data['parents'][0]['name'], c0.name)
        # check children
        self.assertEqual(len(response.data['children']), 2)
        c2_child = next((c for c in response.data['children'] if c['id'] == c2.id), None)
        self.assertIsNotNone(c2_child)
        self.assertEqual(c2_child['id'], c2.id)
        self.assertEqual(c2_child['name'], c2.name)
        # check siblings
        self.assertEqual(len(response.data['siblings']), 1)
        self.assertEqual(response.data['siblings'][0]['id'], c4.id)
        self.assertEqual(response.data['siblings'][0]['name'], c4.name)

    def test_create_category(self):
        category_dict = {
            'name': 'Category 1',
            'children': [
                {
                    'name': 'Category 1.1',
                    'children': [
                        {
                            'name': 'Category 1.1.1',
                            'children': [
                                {'name': 'Category 1.1.1.1'},
                                {'name': 'Category 1.1.1.2'},
                                {'name': 'Category 1.1.1.3'},
                            ]
                        },
                        {
                            'name': 'Category 1.1.2',
                            'children': [
                                {'name': 'Category 1.1.2.1'},
                                {'name': 'Category 1.1.2.2'},
                                {'name': 'Category 1.1.2.3'},
                            ]
                        }
                    ]
                },
                {
                    'name': 'Category 1.2',
                    'children': [
                        {
                            'name': 'Category 1.2.1',
                        },
                        {
                            'name': 'Category 1.2.2',
                            'children': [
                                {'name': 'Category 1.2.2.1'},
                                {'name': 'Category 1.2.2.2'},
                            ]
                        }
                    ]
                }
            ]
        }
        url = reverse('categories-list')
        response = self.client.post(url, data=category_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)