from http import HTTPStatus
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend import dal
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_upload(client: AsyncClient, test_db: AsyncSession):
    response = await client.post(  # type: ignore
        "/files/", files={"file": open("tests/users_posts_audience.csv", "rb")}
    )

    assert response.status_code == HTTPStatus.CREATED

    id = response.json()["id"]
    assert id is not None
    assert response.json()["file_name"] == "users_posts_audience.csv"

    new_csv = await dal.get_csv_file(test_db, id)

    assert new_csv.file_name == "users_posts_audience.csv"
    assert new_csv.id == id


@pytest.mark.asyncio
async def test_file_list(client: AsyncClient, test_db: AsyncSession):
    response = await client.get("/files/")  # type: ignore

    assert response.status_code == HTTPStatus.OK
    print(response.json())
    assert len(response.json()) == 0

    # create few files
    response0 = await client.post(  # type: ignore
        "/files/", files={"file": open("tests/users_posts_audience.csv", "rb")}
    )
    response1 = await client.post(  # type: ignore
        "/files/", files={"file": open("tests/users_posts_audience.csv", "rb")}
    )

    response = await client.get("/files/")  # type: ignore

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2

    assert response.json()[0]['id'] == response1.json()['id'] == 2
    assert response.json()[1]['id'] == response0.json()['id'] == 1


@pytest.mark.asyncio
async def test_get_file(client: AsyncClient, test_db: AsyncSession):

    # create file
    new_file = await client.post(  # type: ignore
        "/files/", files={"file": open("tests/users_posts_audience.csv", "rb")}
    )
    id = new_file.json()['id']

    assert id is not None
    get_file = await client.get(f"/files/{id}")  # type: ignore

    assert get_file.status_code == HTTPStatus.OK
    assert len(new_file.json()) == 6
    assert new_file.json()['columns'] == [
        'impression_id',
        'impression_city',
        'posting_user_id',
        'post_id',
        'viewer_email',
        'impression_country',
        'timestamp',
        'device',
    ]

    get_file = await client.get(f"/files/2")  # type: ignore
    assert get_file.status_code == HTTPStatus.NOT_FOUND
