# from django.test import TestCase

# # Create your tests here.
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User

# class LoginTest(APITestCase):
#     def setUp(self):
#         """
#         Prépare un utilisateur pour les tests de login.
#         """
#         self.username = "testuser"
#         self.password = "testpassword"
#         self.user = User.objects.create_user(username=self.username, password=self.password)
#         self.url = reverse('login')  # Assurez-vous que l'URL correspond à votre URL de login
    
#     def test_login_successful(self):
#         """
#         Test du login réussi avec un utilisateur valide.
#         """
#         data = {
#             'username': self.username,
#             'password': self.password
#         }
#         response = self.client.post(self.url, data, format='json')
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['status'], 'success')
#         self.assertEqual(response.data['message'], 'Utilisateur authentifié avec succès.')

#     def test_login_failed_invalid_credentials(self):
#         """
#         Test du login échoué avec des identifiants invalides.
#         """
#         data = {
#             'username': 'wronguser',
#             'password': 'wrongpassword'
#         }
#         response = self.client.post(self.url, data, format='json')
        
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['status'], 'error')
#         self.assertEqual(response.data['message'], 'Nom d\'utilisateur ou mot de passe incorrect.')
