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
        c1 = Category.objects.create(name='c1')
        c2 = Category.objects.create(name='c2')
        c2.parents.add(c1)
        c2.save()
        c3 = Category.objects.create(name='c3')
        c3.parents.add(c1)
        c3.save()
        c0 = Category.objects.create(name='c0')
        c1.parents.add(c0)
        c1.save()
        c4 = Category.objects.create(name='c4')
        c4.parents.add(c0)
        c4.save()

        url = reverse('category-detail', kwargs={'pk': c1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        root = response.data
        self.assertIn('id', root)
        self.assertIn('name', root)
        self.assertIn('parents', root)
        self.assertIn('children', root)
        self.assertIn('siblings', root)
        # check self
        self.assertEqual(root['id'], c1.id)
        self.assertEqual(root['name'], c1.name)
        # check parents
        self.assertEqual(len(root['parents']), 1)
        self.assertEqual(root['parents'][0]['id'], c0.id)
        self.assertEqual(root['parents'][0]['name'], c0.name)
        # check children
        self.assertEqual(len(root['children']), 2)
        c2_child = next((c for c in root['children'] if c['id'] == c2.id), None)
        self.assertIsNotNone(c2_child)
        self.assertEqual(c2_child['id'], c2.id)
        self.assertEqual(c2_child['name'], c2.name)
        # check siblings
        self.assertEqual(len(root['siblings']), 1)
        self.assertEqual(root['siblings'][0]['id'], c4.id)
        self.assertEqual(root['siblings'][0]['name'], c4.name)

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
        response = self.client.post(url, data=category_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_category = Category.objects.get(id=response.data['id'])
        self.assertEqual(new_category.name, category_dict['name'])
        self.assertEqual(new_category.children.count(), len(category_dict['children']))
        category_1_1 = new_category.children.get(name=category_dict['children'][0]['name'])
        self.assertEqual(category_1_1.children.count(), len(category_dict['children'][0]['children']))

    def test_accept_only_json(self):
        category_dict = {
            'name': 'Category 1',
        }
        url = reverse('categories-list')
        response = self.client.post(url, data=category_dict)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        response = self.client.post(url, data=category_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)