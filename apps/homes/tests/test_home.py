import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Homes
from .serializers import HomeSerializer


class HomeModelTest(APITestCase):
    def setUp(self):
        self.home = Homes.objects.create(
            name="homes estate",
            location="Kindaruma",
            size="1 bedroom",
            price="2.5M",
            status="available"
        )

    def test_home(self):
        """
        This test ensures that the home created in the setUp exists.
        """
        self.assertEqual(self.home.name, "homes estate")
        self.assertEqual(self.home.location, "Kindaruma")
        self.assertEqual(self.home.size, "1 bedroom")
        self.assertEqual(self.home.price, "2.5M")
        self.assertEqual(self.home.status, "available")
        

# test for views

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_home(name="", location="", size="", price="", status=""):
        if name != "" and location != "" and size != "" and price != "" and status != "":
            Homes.objects.create(name=name, location=location, size=size, price=price, status=status)

    def make_a_request(self, kind="post", **kwargs):
        if kind == "post":
            return self.client.post(
                reverse(
                    "homes-list-create",
                    kwargs={
                        "version": kwargs["version"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        elif kind == "put":
            return self.client.put(
                reverse(
                    "homes-detail",
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

    def feth_home(self, pk=0):
        return self.client.get(
            reverse(
                "homes-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def delete_home(self, pk=0):
        return self.client.delete(
            reverse(
                "homes-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def setUp(self):
        self.create_home("Greenspan estate", "Donholm", "2 bedroom", "5M", "completed")
        self.create_home("Embakasi estate", "Embakasi", "3 bedroom", "10M", "completed")
        self.create_home("Garden estate", "Thika Road", "1 bedroom", "7M", "on-going")
        self.valid_data = {
            "name": "test name",
            "location": "test location",
            "size": "test size",
            "price": "test price",
            "status": "test status"
        }
        self.invalid_data = {
            "name": "",
            "location": "",
            "size": "",
            "price": "",
            "status": ""
        }
        self.valid_data = 1
        self.invalid_data = 100


class GetAllHomesTest(BaseViewTest):

    def test_fetch_all_homes(self):
        response = self.client.get(
            reverse("homes-list-create", kwargs={"version": "v1"})
        )
        expected = Homes.objects.all()
        serialized = HomeSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleHomeTest(BaseViewTest):

    def test_fetch_single_home(self):
        res = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        response = self.feth_home(self.valid_home_id)
        expected = Homes.objects.get(pk=self.valid_home_id)
        serialized = HomeSerializer(expected)

        response = self.feth_home(self.invalid_home_id)
        self.assertEqual(
            response.data["message"],
            "Home with id: 100 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateHomeTest(BaseViewTest):

    def test_create_home(self):
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class UpdateHomeTest(BaseViewTest):

    def test_update_home(self):
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=2,
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class DeleteHomeTest(BaseViewTest):
    
    def test_delete_home(self):
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        response = self.delete_home(1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
