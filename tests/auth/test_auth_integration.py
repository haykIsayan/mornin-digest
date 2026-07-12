from tests.auth.test_auth_container import TEST_OTP_CODE


def test_request_otp(client):
    response = client.post(
        "/auth/request-otp",
        json={"otp_recipient": "user@example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "OTP sent"}

def test_verify_otp_invalid_code(client):
    response = client.post(
        "/auth/verify-otp",
        json={"otp_recipient": "user@example.com", "code": "000000"}
    )
    assert response.status_code == 401

def test_verify_otp_creates_user(client):
    response = client.post(
        "/auth/verify-otp",
        json={"otp_recipient": "user@example.com", "code": TEST_OTP_CODE}
    )
    assert response.status_code == 200

    data = response.json()
    assert "user_id" in data
    assert "token" in data
