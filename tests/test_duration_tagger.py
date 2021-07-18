import pytest

from ja_timex.tagger.duration_tagger import DurationTagger


@pytest.fixture(scope="module")
def t():
    return DurationTagger()


def test_normal_date(t):
    pass
