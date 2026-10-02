from rest_framework.throttling import ScopedRateThrottle


class HoldRateThrottle(ScopedRateThrottle):
    scope = "hold"