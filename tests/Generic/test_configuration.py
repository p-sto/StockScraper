"""Tests for Configuration.py"""

import json
import pytest

from StockScraper.Generic.configuration import get_data_from_config


def test_get_data_from_config(fs, mocker):
    # pip install pyfakefs
    fs.CreateFile('test.json')
    fil_content = {"http://www.bankier.pl": ["OPONEO.PL"]}
    fake_json = json.dumps(fil_content)
    mocked = mocker.patch('json.loads')
    mocked.return_value = fake_json
    assert str(get_data_from_config('test.json')) == str(fake_json)
    with pytest.raises(AttributeError) as excinfo:
        get_data_from_config('test')
    excinfo.match('Provided path to config does not exist.')
