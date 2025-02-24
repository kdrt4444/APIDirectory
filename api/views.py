import pandas

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import viewsets, status

from django.db.utils import IntegrityError

from .serializers import MaterialSerializer, CategorySerializer
from .models import Category, Material


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MaterialViewSet(viewsets.ModelViewSet):

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['post'], url_path='load_xlsx')
    def load_xlsx(self, request):
        file = request.FILES.get('file')

        if file is None:
            return Response({'error': 'Файл не загружен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pandas.read_excel(file, engine='openpyxl')

            for _, row in df.iterrows():
                try:
                    Material.objects.create(
                        name=row['Наименование материала'],
                        category=Category.objects.get(id=row['Категория']),
                        code=row['Код материала'],
                        price=row['Стоимость материала']
                    )
                except IntegrityError:
                    pass

            return Response({'message': 'Данные успешно загружены'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
