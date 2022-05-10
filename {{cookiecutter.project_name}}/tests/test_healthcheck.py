import pytest


@pytest.mark.asyncio
async def test_healthcheck(test_client_rest):
    response = await test_client_rest.get("http://test/healthcheck")

    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok"}
