from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from ..serializers import RatingSerializer
from ...models import Rating, PwaAnalytics


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, )

    def update_analytics(self, analytic, rating):
        analytic.rating_avg = (analytic.rating_avg * analytic.rating_count + rating) / (analytic.rating_count + 1)
        analytic.rating_count += 1
        analytic.save()

    def create(self, request, *args, **kwargs):
        data = request.data
        data['created_by'] = {"id": request.user.id}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = Rating(
                pwa_id=data.get('pwa'),
                rating=data.get('rating'),
                comment=data.get('comment'),
                created_by=request.user,
            )
            instance.save()
            analytic = get_object_or_404(PwaAnalytics, pwa_id=data.get('pwa'))
            self.update_analytics(analytic, data.get('rating'))
            response_data = self.get_serializer(instance).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = request.data
        data['created_by'] = {"id": request.user.id}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = get_object_or_404(Rating, id=kwargs.get('pk'))
            # update analytics first
            analytic = get_object_or_404(PwaAnalytics, pwa=instance.pwa)
            if analytic.rating_count == 1:
                analytic.rating_count = 0
                analytic.rating_avg = 0
            else:
                analytic.rating_avg = (analytic.rating_avg * analytic.rating_count - instance.rating) / (analytic.rating_count - 1)
                analytic.rating_count -= 1

            instance.comment = data.get('comment')
            instance.rating = data.get('rating')
            instance.save()
            self.update_analytics(analytic, data.get('rating'))
            response_data = self.get_serializer(instance).data
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
