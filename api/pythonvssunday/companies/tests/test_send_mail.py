from unittest.mock import patch

from django.test import TestCase
from django.core.mail import send_mail
from django.conf import settings

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


def test_send_email_should_succed(settings, mailoutbox):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    assert len(mailoutbox) == 0
    send_mail(
        subject="Test Subject",
        from_email="test_sender@add.com",
        recipient_list=["recipient@add.com"],
        message="test message",
    )
    print(f"{mailoutbox[0].message=}")
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Test Subject"
    # assert mailoutbox[0].message == "test message"


def test_send_email_without_arguments_should_send_empty_mail(client):
    with patch(
            "api.pythonvssunday.companies.views.send_mail"
    ) as mocked_send_mail_function:
        response = client.post(path="/send_company_email")
        assert response.status_code == 200
        mocked_send_mail_function.assert_called_with(
            subject=None,
            message=None,
            from_email=EMAIL_HOST_USER,
            recipient_list=[EMAIL_HOST_USER],
        )


def test_send_email_with_get_verb_should_fail(client):
    with patch(
            "api.pythonvssunday.companies.views.send_mail"
    ) as mocked_send_mail_function:
        response = client.get(path="/send_company_email")
        assert response.status_code == 405
        mocked_send_mail_function.assert_not_called()
