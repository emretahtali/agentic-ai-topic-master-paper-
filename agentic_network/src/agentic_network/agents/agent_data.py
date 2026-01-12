from typing import Literal

from agentic_network.utils import get_class_field_values


class AgentData:
    class Agents:
        add_alarm = "AddAlarm"
        buy_bus_ticket = "BuyBusTicket"
        find_attractions = "FindAttractions"
        find_bus = "FindBus"
        find_provider = "FindProvider"
        get_alarms = "GetAlarms"
        lookup_music = "LookupMusic"
        none = "NONE"
        play_media = "PlayMedia"
        reserve_hotel = "ReserveHotel"
        reserve_restaurant = "ReserveRestaurant"
        search_hotel = "SearchHotel"
        search_house = "SearchHouse"
        search_roundtrip_flights = "SearchRoundtripFlights"

    agent_list = get_class_field_values(Agents)
    agent_literals = Literal[*agent_list]

