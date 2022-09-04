import pytest
from dags.api_load.scripts.load import load


def test_load(mocker):
    resp_return_value = [
        {
            'ad_id': '7b4ae984-a4a6-4a43-8c07-a3e28ec04a4a',
            'ad_group': 'brand',
            'ad_campaign': '__unknown',
            'shown_at': 1662018683.8688061,
            },
        {
            'ad_id': '52d61493-4172-4c15-aaaa-24d17715f3db',
            'ad_group': 'marketing',
            'ad_campaign': 899,
            'shown_at': 1661956595.8688061,
            'ad_scheme': {'origin': 'manual', 'approved': True},
            }
        ]
    mocker.patch('dags.api_load.scripts.load.get_api_response',
                 return_value=resp_return_value)
    mocker.patch('dags.api_load.scripts.load.upload_to_s3',
                 return_value=None)
    mocker.patch('dags.api_load.scripts.load.insert_to_db',
                 return_value=None)
    expected_data = [{'ad_id': '7b4ae984-a4a6-4a43-8c07-a3e28ec04a4a', 'ad_group': 'brand', 'ad_campaign': -1, 'shown_at': '2022-09-01 07:51:23', 'ad_scheme': 'null'}, {'ad_id': '52d61493-4172-4c15-aaaa-24d17715f3db', 'ad_group': 'marketing', 'ad_campaign': 899, 'shown_at': '2022-08-31 14:36:35', 'ad_scheme': '{"origin": "manual", "approved": true}'}]
    assert load() == expected_data
