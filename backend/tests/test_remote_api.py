from http import HTTPStatus
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_new_file_from_api(client: AsyncClient, test_db: AsyncSession):
    response = await client.post(  # type: ignore
        "/remote_api/", params={"url": "https://jsonplaceholder.typicode.com/posts/"}
    )

    assert response.status_code == HTTPStatus.CREATED

    id = response.json()["id"]
    assert id is not None

    assert response.json()['url'] == "https://jsonplaceholder.typicode.com/posts/"
    assert response.json()['columns'] == ['userId', 'id', 'title', 'body']


@pytest.mark.asyncio
async def test_enrich_csv_with_new_data(client: AsyncClient, test_db: AsyncSession):

    # create csv file

    response = await client.post(  # type: ignore
        "/files/", files={"file": open("tests/users_posts_audience.csv", "rb")}
    )

    assert response.status_code == HTTPStatus.CREATED
    file0 = response.json()

    # create data from remote API
    response = await client.post(  # type: ignore
        "/remote_api/", params={"url": "https://jsonplaceholder.typicode.com/posts/"}
    )

    assert response.status_code == HTTPStatus.CREATED
    file1 = response.json()

    # now, lets make some noise!

    response = await client.post(  # type: ignore
        "/remote_api/extend",
        params={
            "url": "https://jsonplaceholder.typicode.com/posts/",
            "csv_id": file0["id"],
            "csv_column": "post_id",
            "api_column": "id",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert file0['columns'] == [
        'impression_id',
        'impression_city',
        'posting_user_id',
        'post_id',
        'viewer_email',
        'impression_country',
        'timestamp',
        'device',
    ]
    assert file1['columns'] == ['userId', 'id', 'title', 'body']
    assert response.json()['columns'] == [
        'impression_id',
        'impression_city',
        'posting_user_id',
        'post_id',
        'viewer_email',
        'impression_country',
        'timestamp',
        'device',
        'userId',
        'id',
        'title',
        'body',
    ]
