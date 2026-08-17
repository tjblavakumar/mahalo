import pytest

from backend.utils.reset_data import reset_demo_data


@pytest.fixture(scope="session", autouse=True)
def reset_database_for_test_session():
    reset_demo_data()
    yield
