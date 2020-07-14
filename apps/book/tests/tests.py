import json
from django.test import TestCase
from djago.urls import reverse
from rest_frawork.test import APITestCase, APIClient
from rest_frawork.views import status
from .models import Book
from .serializers import BookSerializer


class BookModelTest(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            user="1",
            home="estate",
            amount="2M"
        )

    def test_book(self):
        """
        This test ensures that the book created is the setup exists.
        """
        self.assertEqual(self.book.amount, "2M")
        self.assertEqual(self.book.user, "1")
        self.assertEqual(self.book.home, "estate")
        
class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_book(user="", home="", amount=""):
        if user != "" and home != "" and amount != "":
            Book.objects.create(user=user, home=home, amount=amount)

    def make_request(self, kind="post", **kwargs):
        if kind == "post":
            return self.client.post(
                reverse(
                    "books-list-create",
                    kwargs={
                        "version": kwargs["version"]
                    }
                ),
                data=json.dumps(kwargs["data"])
                content_type='application/json'
            )

        elif kind == "put":
            return self.client.put(
                reverse(
                    "book-detail",
                    kwargs={
                        "version": kwargs["version"],
                        "pk": kwargs["id"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        else:
            return None

    def fetch_book(self, pk=0):
        return self.client.get(
            reverse(
                "book-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def delete_book(self, pk=0):
        return self.client.delete(
            reverse(
                "book-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def setUp(self):
        self.create_book("1" "Greenspan estate", "2M")
        self.create_home("3", "Embakasi estate", "3M")
        self.create_home("2", "Garden estate", "1M")
        self.valid_data = {
            "user": "test user",
            "home": "test home",
            "amount": "test amount",
        }
        self.invalid_data = {
            "user": "",
            "home": "",
            "amount": ""
        }
        self.valid_data = 1
        self.invalid_data = 100


class AllBookTest(BaseViewTest):

    def test_fetch_all_books(self):
        response = self.client.get(
            reverse("books-list-create", kwargs={"version": "v1"})
        )
        expected = Book.objects.all()
        serialized = BookSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SingleBookTest(BaseViewTest):

    def test_fetch_single_book(self):
        res = self.make_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        response = self.fetch_book(self.valid_book_id)
        expected = Book.objects.get(pk=self.valid_book_id)
        serialized = BookSerializer(expected)

        response = self.fetch_book(self.invalid_book_id)
        self.assertEqual(
            response.data["message"],
            "Book with id: 100 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateBookTest(BaseViewTest):

    def test_create_book(self):
        response = self.make_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateBookTest(BaseViewTest):

    def test_update_book(self):
        response = self.make_request(
            kind="put",
            version="v1",
            id=2,
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteBookTest(BaseViewTest):
    
    def test_delete_book(self):
        response = self.make_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        response = self.delete_book(1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        