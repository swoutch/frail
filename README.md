frail - search french trains
========================================================

This package search trains on oui.sncf, the SNCF website to buy train tickets (SNCF is the main french railway company).

You can install it with:

    pip install frail

Example:

    >>> import frail, pendulum
    >>> trains = frail.search("FRPAR", "FRMRS", timestamp=pendulum.now())
