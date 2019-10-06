import json
from unittest.mock import Mock, patch

import pendulum

import frail


@patch("requests.post")
def test_search(mock_post):

    # configure requests.post to return fake test data
    response_mock = Mock()
    with open("tests/unit/sample_response.json") as file:
        response_mock.json = Mock(return_value=json.load(file))
    mock_post.return_value = response_mock

    # calling function we want to test
    actual = frail.search(
        origin="FRPAR", destination="FRMRS", timestamp=pendulum.datetime(2019, 10, 5, 6)
    )
    # was requests.post called with the right args ?
    mock_post.assert_called_with(
        "https://www.oui.sncf/proposition/rest/travels/outward/train",
        data=json.dumps(
            {
                "wish": {
                    "context": {"sumoForTrain": {"eligible": True}},
                    "mainJourney": {
                        "abroadJourney": False,
                        "destination": {"code": "FRMRS"},
                        "origin": {"code": "FRPAR"},
                    },
                    "passengers": [{"typology": "YOUNG"}],
                    "salesMarket": "fr-FR",
                    "schedule": {
                        "inwardType": "DEPARTURE_FROM",
                        "outward": "2019-10-05T06:00:00",
                        "outwardType": "DEPARTURE_FROM",
                    },
                    "travelClass": "SECOND",
                }
            }
        ),
        headers={"Content-Type": "application/json"},
    )

    # does the API return 2 trains ?
    assert len(actual) == 2

    # test of the 1st train
    assert actual[0].origin == "FRPLY"
    assert actual[0].destination == "FRMSC"
    assert actual[0].departure == pendulum.datetime(
        2019, 10, 5, 6, 12, tz="Europe/Paris"
    )
    assert actual[0].arrival == pendulum.datetime(2019, 10, 5, 9, 26, tz="Europe/Paris")
    assert actual[0].price == 45

    # test of the 2nd train
    assert actual[1].origin == "FRPLY"
    assert actual[1].destination == "FRMSC"
    assert actual[1].departure == pendulum.datetime(
        2019, 10, 5, 7, 10, 50, tz="Europe/Paris"
    )
    assert actual[1].arrival == pendulum.datetime(
        2019, 10, 5, 10, 11, 34, tz="Europe/Paris"
    )
    assert actual[1].price == 12
