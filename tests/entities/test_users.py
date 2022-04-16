from digitaltwin.client import DigitalTwinClient


def test_user_fetch():
    client = DigitalTwinClient(
        "EbDNqD6IThQoR0Kcre72fq3GW52rMAVQvoxTOWuEmSbdh8Cw83pgcxXcLVXbR4Ad",
        user_uuid="ed8a5f44-5094-4950-a214-33d7241471b6",
    )
    client.fetch_user()
