import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Profile
from .serializers import ProfileSerializer



class ProfileModelTest(APIClient):
    def setUp(self):
        self.profile = Profile.objects.create(
            personal_identification="00221177",
            bio="I am a software developer",
            phone_number="254700223367",
            birth_date="2020-07-14"
        )

    def test_profile(self):
        """
        This test ensures that the song created in the setUp exists.
        """
        self.assertEqual(self.profile.personal_identification, "00221177")
        self.assertEqual(self.profile.bio, "I am a software developer")
        self.assertEqual(self.profile.phone_number, "254700223367")
        self.assertEqual(self.profile.birth_date, "2020-07-14")



class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_profile(personal_identification="", bio="", phone_number="", birth_date=""):
        if personal_identification != "" and bio != "" and phone_number != "" and birth_date != "":
            Profile.objects.create(personal_identification=personal_identification, bio=bio, phone_number=phone_number, birth_date=birth_date)

    def make_a request(self, kind="post", **kwargs):
        if kind == "post":
            return self.client.post(
                reverse(
                    "profile-list-create",
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
                    "profile-detail",
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

    def fetch_profile(self, pk=0):
        return self.client.get(
            reverse(
                "profile-detail",
                kwargs={
                    "version": "v1",
                    "pk":pk
                }
            )
        )

    def delete_profile(self, pk=0):
        return self.client.delete(
            reverse(
                "profile-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def setUp(self):
        # add test data
        self.create_profile("22553311", "I like music", "25467251434", "2014-07-11")
        self.create_profile("33770099", "I love cooking", "25476254900", "2019-04-12")
        self.create_profile("22887712", "I like hiking", "25488906712", "2016-01-11")
        self.create_profile("33559912", "I love movies", "25433880134", "2018-08-21")
        self.valid_data ={
            "personal_identification": "22334455",
            "bio": "test bio",
            "phone_number": "254722118812",
            "birth_date": "2016-05-12"
        }
        self.invalid_data = {
            "personal_identification": "",
            "bio": "",
            "phone_number": "",
            "birth_date": ""
        }
        self.valid_song_id = 1
        self.invalid_song_id = 100



class GetAllProfiles(BaseViewTest):

    def test_get_all_profiles(self):
        """
        This test ensures that all profiles added in the setUp method
        exist when we make a GET request to the profile/ endpoint.
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("profile-list-create", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Profile.objects.all()
        serialized = ProfileSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetASingleProfileTest(BaseViewTest):
    
    def test_get_single_profile(self):
        """
        This test ensures that a single profile of a given id is returned.
        """
        res = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        response = self.fetch_profile(self.valid_profile_id)
        # fetch the data from db
        expected = Profile.objects.get(pk=self.valid_profile_id)
        serialized = ProfileSerializer(expected)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a profile that does not not exist
        response = self.fetch_profile(self.invalid_profile_id)
        self.assertEqual(
            response.data["message"],
            "Profile with id: 100 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AddProfileTest(BaseViewTest):

    def test_create_song(self):
        """
        This test ensures that a single profile can be added.
        """
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

class UpdateSongsTest(BaseViewTest):

    def test_update_song(self):
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=2,
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      

class DeleteSongsTest(BaseViewTest):

    def test_delete_song(self):
        """
        This test ensures that when a profile of given id can be deleted.
        """
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        response = self.delete_profile(1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
