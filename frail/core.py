"""
    How to use it:
    >>> import frail, pendulum
    >>> trains = frail.search("FRPAR", "FRMRS", timestamp=pendulum.now())
"""
import json

import pendulum
import requests

import frail.train

__all__ = ["search"]


def search(origin, destination, timestamp):
    """
        Returns list of trains objects around specified timestamp.
    """

    response = requests.post(
        "https://www.oui.sncf/proposition/rest/travels/outward/train",
        data=json.dumps(
            {
                "wish": {
                    "context": {"sumoForTrain": {"eligible": True}},
                    "mainJourney": {
                        "abroadJourney": False,
                        "destination": {"code": destination},
                        "origin": {"code": origin},
                    },
                    "passengers": [{"typology": "YOUNG"}],
                    "salesMarket": "fr-FR",
                    "schedule": {
                        "inwardType": "DEPARTURE_FROM",
                        "outward": timestamp.format("YYYY-MM-DDTHH:mm:ss"),
                        "outwardType": "DEPARTURE_FROM",
                    },
                    "travelClass": "SECOND",
                }
            }
        ),
        headers={"Content-Type": "application/json"},
    )

    trains = []
    for travel in response.json()["travelProposals"]:
        train = frail.train.Train(
            origin=travel["origin"]["station"]["metaData"]["MI"]["code"],
            destination=travel["destination"]["station"]["metaData"]["MI"]["code"],
            departure=pendulum.parse(travel["departureDate"], tz="Europe/Paris"),
            arrival=pendulum.parse(travel["arrivalDate"], tz="Europe/Paris"),
            price=travel["minPrice"],
        )
        trains.append(train)
    return trains
