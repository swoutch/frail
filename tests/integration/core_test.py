import pendulum

import frail


def test_search():
    trains = frail.search("FRPAR", "FRMRS", timestamp=pendulum.now(tz="Europe/Paris"))
    assert len(trains) > 0
    assert trains[0].price >= 0
