from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from models import SuppressedList


class AddEmailTests(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        obj = SuppressedList(email='shashank.shekhar@vgmail.in', blocked_date='2015-01-07T17:13:50.620Z')
        obj.save()


    def test_adding_new_email(self):
        """
            Ensure we can create a email entry in Suppressed List
        """
        url = reverse('add_email')
        data = {
            "notificationType": "Bounce",
            "bounce": {
                "bounceSubType": "General",
                "bounceType": "Transient",
                "bouncedRecipients": [{
                                          "emailAddress": "shashank.shekhar@vgmail.in",
                                          "status": "5.0.0",
                                          "action": "failed",
                                          "diagnosticCode": "smtp; 503 5.0.0 Permanent Failure"
                                      },
                                      {
                                          "emailAddress": "jiteshsharma@vgmail.in",
                                          "status": "5.0.0",
                                          "action": "failed",
                                          "diagnosticCode": "smtp; 503 5.0.0 Permanent Failure"},
                                      {
                                          "emailAddress": "arvindtomar@vgmail.in",
                                          "status": "5.0.0",
                                          "action": "failed",
                                          "diagnosticCode": "smtp; 503 5.0.0 Permanent Failure"
                                      }],
                "reportingMTA": "dsn; a8-19.smtp-out.amazonses.com",
                "timestamp": "2015-01-07T17:13:50.620Z",
                "feedbackId": "0000014ac5635aa6-c30f5917-4437-4d84-bd75-26088600078a-000000"
            },
            "mail": {
                "timestamp": "2015-01-07T17:13:49.000Z",
                "destination": ["shashank.shekhar@vgmail.in", "jiteshsharma@vgmail.in", "arvindtomar@vgmail.in"],
                "messageId": "0000014ac56355cf-c5d515ba-1bcf-484d-a5b4-3701454b0053-000000",
                "source": "wms-reports@delhivery.com"
            }}
        return_data = {'success': True, 'error': False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, return_data)

    def test_check_email(self):
        """
            Ensure we can check the status of supressed list email

        """
        url = reverse('check_email')
        data = {"emails": ["shashank.shekhar@vgmail.in"]}
        response_data = {"results": [{"email": "shashank.shekhar@vgmail.in", "blocked": False}], "success": True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)