from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Document
from .serializers import DocSerializer
from .dcml_convertor_gsb import GsbConversionDoc
from .replacers import body_decoder


# Create your views here.
@api_view(['GET'])
def get_routes(request):
    routes = [
        {
            "endpoint": '/docs/',
            "method": "GET",
            "body": None,
            "description": 'Returns all documents in the database'
        }
    ]

    return Response(routes)

@api_view(['GET'])
def get_docs(request):
    docs = Document.objects.all()

    serializer = DocSerializer(docs, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_doc(request, pk):
    doc = Document.objects.get(id=pk)
    serializer = DocSerializer(doc, many=False)

    print(serializer.data)

    return Response(serializer.data)

@api_view(['POST'])
def create_doc(request):
    data = request.data

    body_data = body_decoder(data['body'])

    doc = Document.objects.create(
        name=data['name'],
        body=body_data
    )
    serializer = DocSerializer(doc, many=False)
    
    return Response(serializer.data)
    
@api_view(['PUT'])
def update_doc(request, pk):
    data = request.data
    doc = Document.objects.get(id=pk)

    if data.get('name') is None:
        data["name"] = doc.name

    serializer = DocSerializer(doc, data=data)
    if serializer.is_valid():
        serializer.save()

        setattr(doc, 'body', body_decoder(str(data['body'])))
        doc.save()

    print(data)
        
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_doc(request, pk):
    doc = Document.objects.get(id=pk)
    doc.delete()

    return Response(f"The {pk}. Document has been deleted successfully")

@api_view(['GET'])
def convert_doc(request, pk):
    wordDoc = GsbConversionDoc()
    doc = Document.objects.get(id=pk)

    wordDoc.parse(doc.body)
    wordDoc.convert()
    wordDoc.save('api/output/')

    return Response('Document converted successfully')
    
@api_view(['GET'])
def latest_doc(request):
    doc = Document.objects.latest('created')
    serializer = DocSerializer(doc, many=False)

    return Response(serializer.data)
