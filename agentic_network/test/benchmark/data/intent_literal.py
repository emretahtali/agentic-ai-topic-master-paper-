from typing import Literal

intent_literal = Literal[
    "AddAlarm", "BookAppointment", "BookHouse",
    "BuyBusTicket", "BuyEventTickets", "BuyMovieTickets",
    "FindAttractions", "FindBus", "FindEvents",
    "FindHomeByArea", "FindMovies", "FindProvider",
    "FindRestaurants", "FindTrains",
    "GetAlarms", "GetCarsAvailable", "GetRide"
]