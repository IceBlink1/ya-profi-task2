from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from notes.models import Note, NoteSerializer
from ya_profi_notes.settings import MAX_SYMBOLS


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def notes(request):
    if request.method == 'GET':
        notes = Note.objects.all()

        for i in range(len(notes)):
            if notes[i].title is None or len(notes[i].title) == 0:
                notes[i].title = notes[i].content[:MAX_SYMBOLS]

        title = request.query_params.get('string', None)
        if title is not None:
            notes_title = [notes.filter(title__icontains=title), notes.filter(content__icontains=title)]
            res = []
            for i in notes_title:
                for j in i:
                    if j not in res:
                        res.append(j)
            notes = res

        note_serializer = NoteSerializer(notes, many=True)
        return JsonResponse(note_serializer.data, safe=False)
    elif request.method == 'POST':
        content = request.data.get('content')
        note = Note()
        note.content = content
        note.title = request.data.get('title')
        note.save()
        note_serializer = NoteSerializer(note)
        return JsonResponse(note_serializer, safe=False, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def note_detail(request, pk):
    if request.method == 'GET':
        note = Note.objects.all().filter(pk=pk)
        if note is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if note.title is None or len(note.title) == 0:
            note.title = note.content[:MAX_SYMBOLS]
        note_serializer = NoteSerializer(note)
        return JsonResponse(note_serializer.data)

    elif request.method == 'PUT':
        note = Note.objects.all().filter(pk=pk)
        if note is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        note_data = JSONParser().parse(request)
        note_serializer = NoteSerializer(note, data=note_data)
        if note_serializer.is_valid():
            note_serializer.save()
            return JsonResponse(note_serializer.data)
        return JsonResponse(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        note = Note.objects.all().filter(pk=pk)
        if note is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class NoteView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    pagination_class = LimitOffsetPagination

    class Meta:
        model = Note
        fields = ('content', 'title', 'date', 'user')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = Note.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        content = request.data.get('content')
        note = Note()
        note.content = content
        note.title = request.data.get('title')
        note.save()
        return Response(note)
