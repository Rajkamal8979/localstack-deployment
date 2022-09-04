import random
import time
import uuid


def _generate_ad():
    random_number = random.random()

    result = {
        "ad_id": str(uuid.uuid4()),
        "ad_group": random.choice(["marketing", "recruiting", "brand", "investment"]),
        "ad_campaign": int(random_number * 1000) if random_number > 0.5 else "__unknown",
        "shown_at": time.time() - int(random_number * 100000),
    }

    if random_number > 0.8:
        result["ad_scheme"] = {
            "origin": random.choice(["manual", "automatic"]),
            "approved": random_number > 0.7,
        }

    return result


def get_api_response():
    """
    This method generates a mock api response for the purpose of this coding exercise
    Please use this method as if it was calling a 3rd party HTTP api and returning the response.
    Do not adjust this method. Take it as given by a 3rd party tool.
    """
    return [_generate_ad() for n in range(100)]
