import django_filters
from .models import Doctor

class DoctorFilter(django_filters.FilterSet):
    # Filter by price range (min and max)
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')  # Minimum price
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')  # Maximum price
    
    # Filter by location (case-insensitive search)
    location = django_filters.CharFilter(lookup_expr='icontains')  # Location contains
    
    # Filter by speciality (search by speciality name)
    speciality = django_filters.CharFilter(field_name='speciality__name', lookup_expr='icontains')  # Speciality name contains
    
    # Filter by availability (True/False)
    availability = django_filters.BooleanFilter(field_name='availability', method='filter_availability')
    
    # Filter by insurance (True/False)
    insurance_accepted = django_filters.BooleanFilter(field_name='insurance_accepted', method='filter_insurance')
    
    class Meta:
        model = Doctor
        fields = ['price_min', 'price_max', 'location', 'speciality', 'availability', 'insurance_accepted']
        
    def filter_availability(self, queryset, name, value):
        # Filter by availability (True or False)
        return queryset.filter(availability=value)
    
    def filter_insurance(self, queryset, name, value):
        # Filter by whether insurance is accepted (True or False)
        return queryset.filter(insurance_accepted=value)
