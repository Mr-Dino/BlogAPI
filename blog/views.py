from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from django.db.models import Q
from .models import Post, Comment
from .serializers import PostCreateSerializer, CommentCreateSerializer


@api_view(['GET'])
def get_post_comments(request, post_id):
    """Получение комментариев до 4 уровня (не включительно)"""
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(Q(post=post_id) & Q(level__lt=4))
    all_data = []
    json_data = {"count": len(comments) + 1}
    all_data.append(post.get_dict())
    for comment in comments:
        if comment.level == 1:
            # обработка комментариев 1 уровня
            all_data[0]["comments"].append(comment.get_dict())
        else:
            # обработка комментариев, имеющих родителей
            for i in range(0, len(all_data[0]["comments"])):
                if str(comment.parent) == str(all_data[0]["comments"][i]["id"]):
                    # обработка комментариев 2 уровня
                    all_data[0]["comments"][i]['child'].append(comment.get_dict())
                else:
                    # обработка комментариев 3 уровня
                    for y in range(0, len(all_data[0]["comments"][i]["child"])):
                        if str(comment.parent) == str(all_data[0]["comments"][i]["child"][y]["id"]):
                            all_data[0]["comments"][i]['child'][y]["child"].append(comment.get_dict())
    json_data["data"] = all_data
    return JsonResponse(json_data)


@api_view(["GET"])
def get_all_comments(request, comment_id):
    """
    Получение комментариев дальше 3 уровня вложенности.
    Решил создать собственный метод, так как при использовании возможностей rest_framework
    генератор будет постоянно обращаться в базу и соответственно количество запросов возрастет
    """
    main_comment = Comment.objects.get(pk=comment_id)
    comments = Comment.objects.filter(Q(post=main_comment.post) & Q(level__gt=3)).order_by('-level')
    all_data = []
    json_data = {}
    max_lvl, has_next = get_max_level(comments, main_comment.id)
    levels = {}
    previous_data = []
    if has_next:
        # проверка на наличие детей у главного комментария
        for comment in comments:
            # сбор комментариев по уровням
            if str(comment.level) not in levels:
                levels[str(comment.level)] = [comment.get_dict()]
            else:
                levels[str(comment.level)].append(comment.get_dict())
        levels[main_comment.level] = [main_comment.get_dict()]
        for data in levels:
            # обход дерева, начиная с веток
            for i in range(0, len(levels[data])):
                if not previous_data:
                    previous_data = ([len(levels[data]), levels[data]])
                for y in range(0, previous_data[0]):
                    if str(levels[data][i]['id']) == str(previous_data[1][y]['parent']):
                        levels[data][i]['child'].append(previous_data[1][y])
            previous_data = ([len(levels[data]), levels[data]])
        json_data['data'] = levels[3]
        return JsonResponse(json_data)
    else:
        json_data = {'data': all_data.append(main_comment.to_dict())}
        return JsonResponse(json_data)


def get_max_level(comments, id):
    """Получает максимальный уровень вложенности и провереят есть ли вообще дети у комментария"""
    level = 3
    has_next = False
    for comment in comments:
        if comment.level > level:
            level = comment.level
        if id == comment.parent.id:
            has_next = True
    return level, has_next


@api_view(['POST'])
def create_post(request):
    """Функция для создания поста"""
    if request.method == 'POST':
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_comment(request):
    """Функция для создания комментария к посту или комментария к коментарию любого уровня вложенности"""
    if request.method == 'POST':
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
