from rest_framework import generics, permissions
from .serializers import CustomerRegisterSerializer, ProviderRegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .throttles import LoginRateThrottle

class CustomerRegisterView(generics.CreateAPIView):
    serializer_class = CustomerRegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginRateThrottle]


class ProviderRegisterView(generics.CreateAPIView):
    serializer_class = ProviderRegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginRateThrottle]
    
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user    
    

class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]    