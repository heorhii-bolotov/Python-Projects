"""
    Json Schema variant
"""
# import json
#
# from django.contrib.auth import authenticate
#
#
# from django.http import HttpResponse, JsonResponse
# from django.views import View
#
# from marshmallow import Schema, ValidationError, fields, post_load
# from marshmallow.validate import Length, Range
#
# from .models import Item, Review
#
# import base64
#
#
# class ItemSchema(Schema):
#     id = fields.Int(dump_only=True)
#     title = fields.Str(required=True, validate=Length(1, 64))
#     description = fields.Str(required=True, validate=Length(1, 1024))
#     price = fields.Int(required=True, validate=Range(1, 1000000), strict=True)
#
#     @post_load
#     def make(self, data):
#         return Item(**data)
#
#
# class ReviewSchema(Schema):
#     id = fields.Int(dump_only=True)
#     grade = fields.Int(required=True, validate=Range(1, 10), strict=True)
#     text = fields.Str(required=True, validate=Length(1, 1024))
#
#     @post_load
#     def make(self, data):
#         return Review(**data)
#
#
# def get_authorization_header(request):
#     """
#         :return request's 'Authorization: ' header, as tuple of login, password
#     """
#
#     auth = request.META.get('HTTP_AUTHORIZATION', b'')
#     if isinstance(auth, str):
#         auth = base64.b64encode(auth)
#
#     parts = base64.b64decode(auth).split()
#     auth = tuple(parts[1].partition(':'))
#
#     return auth
#
#
# def authenticate_credentials(user_id, password):
#     """
#         Authenticate the user_id and password
#     """
#     user = authenticate(username=user_id, password=password)
#     return user
#
#
# class AddItemView(View):
#     """View РґР»СЏ СЃРѕР·РґР°РЅРёСЏ С‚РѕРІР°СЂР°."""
#
#     def post(self, request):
#         try:
#             login, password = get_authorization_header(request)
#             user = authenticate_credentials(login, password)
#             if not user:
#                 return JsonResponse({}, 401)
#             if not user.is_staff():
#                 return JsonResponse({}, 403)
#         except (TypeError, UnicodeDecodeError):
#             return JsonResponse({}, 404)
#
#         try:
#             document = json.loads(request.body)
#             schema = ItemSchema(strict=True)
#             item = schema.load(document).data
#             item.save()
#         except (json.JSONDecodeError, ValidationError, AssertionError):
#             return HttpResponse(status=400)
#         data = {'id': item.pk}
#         return JsonResponse(data, status=201)
#
#
# class PostReviewView(View):
#     """View РґР»СЏ СЃРѕР·РґР°РЅРёСЏ РѕС‚Р·С‹РІР° Рѕ С‚РѕРІР°СЂРµ."""
#
#     def post(self, request, item_id):
#         try:
#             item = Item.objects.get(pk=item_id)
#             document = json.loads(request.body)
#             schema = ReviewSchema(strict=True)
#             review = schema.load(document).data
#             review.item = item
#             review.save()
#         except Item.DoesNotExist:
#             return HttpResponse(status=404)
#         except (json.JSONDecodeError, ValidationError):
#             return HttpResponse(status=400)
#         data = {'id': review.pk}
#         return JsonResponse(data, status=201)
#
#
# class GetItemView(View):
#     """View РґР»СЏ РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё Рѕ С‚РѕРІР°СЂРµ.
#
#     РџРѕРјРёРјРѕ РѕСЃРЅРѕРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё РІС‹РґР°РµС‚ РїРѕСЃР»РµРґРЅРёРµ РѕС‚Р·С‹РІС‹ Рѕ С‚РѕРІР°СЂРµ, РЅРµ Р±РѕР»РµРµ 5
#     С€С‚СѓРє.
#     """
#
#     def get(self, request, item_id):
#         try:
#             item = Item.objects.get(pk=item_id)
#         except Item.DoesNotExist:
#             return HttpResponse(status=404)
#         schema = ItemSchema()
#         data = schema.dump(item).data
#         query = Review.objects.filter(item=item).order_by('-id')
#         reviews = query[:5]
#         schema = ReviewSchema(many=True)
#         data['reviews'] = schema.dump(reviews).data
#         return JsonResponse(data, status=200)
#
# import json
#
# from django.contrib.auth import authenticate
# from jsonschema import validate
# from jsonschema.exceptions import ValidationError
#
# from django.http import HttpResponse, JsonResponse
# from django.views import View
#
# from .models import Item, Review
#
# from django.core.exceptions import ObjectDoesNotExist
#
# from django.shortcuts import render
#
# import base64
#
# ADD_ITEM_SCHEME = {
#     '$schema': 'http//:json-schema.org/schema#',
#     'type': 'object',
#     'properties': {
#         'title': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 64,
#         },
#         'description': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 1024,
#         },
#         'price': {
#             'type': 'integer',
#             'minimum': 1,
#             'maximum': 1000000,
#         }
#     },
#     'required': ['title', 'description', 'price']
# }
#
# POST_REVIEW_SCHEME = {
#     '$schema': 'http//:json-schema.org/schema#',
#     'type': 'object',
#     'properties': {
#         'text': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 1024,
#         },
#         'grade': {
#             'type': 'integer',
#             'minimum': 1,
#             'maximum': 10,
#         }
#     },
#     'required': ['title', 'description', 'price']
# }
#
#
# def get_authorization_header(request):
#     """
#         :return request's 'Authorization: ' header, as tuple of login, password
#     """
#
#     auth = request.META.get('HTTP_AUTHORIZATION', b'')
#     if isinstance(auth, str):
#         auth = base64.b64encode(auth)
#
#     parts = base64.b64decode(auth).split()
#     auth = tuple(parts[1].partition(':'))
#
#     return auth
#
#
# def authenticate_credentials(user_id, password):
#     """
#         Authenticate the user_id and password
#     """
#     user = authenticate(username=user_id, password=password)
#     return user
#
#
# # Create your views here.
# class AddItemView(View):
#     """View для создания товара."""
#
#     def post(self, request):
#         try:
#             login, password = get_authorization_header(request)
#             user = authenticate_credentials(login, password)
#             if not user:
#                 return JsonResponse({}, 401)
#             if not user.is_staff():
#                 return JsonResponse({}, 403)
#         except (TypeError, UnicodeDecodeError):
#             return JsonResponse({}, 404)
#
#         # Здесь должен быть ваш код
#         try:
#             document = json.loads(request.body)
#             validate(document, ADD_ITEM_SCHEME)
#             resp = self.add_item(document)
#
#             return JsonResponse(resp, status=201)
#
#         except json.JSONDecodeError:
#             return JsonResponse({}, status=400)
#         except ValidationError:
#             return JsonResponse({}, status=400)
#
#     @staticmethod
#     def add_item(document):
#         # Does not check validity of the doc
#         new_item = Item.objects.create(title=document['title'],
#                                        description=document['description'],
#                                        price=document['price'])
#         # {'id': new_item.objects.id}
#         return {'id': new_item.id}
#
#
# class PostReviewView(View):
#     """View для создания отзыва о товаре."""
#
#     def post(self, request, item_id):
#         # Здесь должен быть ваш код
#         try:
#             document = json.loads(request.body)
#             validate(document, POST_REVIEW_SCHEME)
#             resp = self.add_item_review(item_id, document)
#
#             return JsonResponse(resp, status=201)
#
#         except json.JSONDecodeError:
#             return JsonResponse({}, status=400)
#         except ValidationError:
#             return JsonResponse({}, status=400)
#         except ObjectDoesNotExist:
#             return JsonResponse({}, status=404)
#
#     @staticmethod
#     def add_item_review(item_id, document):
#         # Throws Exception if item_id does not exist
#         # Does not check validity of the doc
#         item = Item.objects.get(id=item_id)
#         review = Review.objects.create(
#             grade=document['grade'],
#             text=document['text'],
#             item=item
#         )
#
#         return {'id': review.id}
#
#
# class GetItemView(View):
#     """View для получения информации о товаре.
#
#     Помимо основной информации выдает последние отзывы о товаре, не более 5
#     штук.
#     """
#
#     def get(self, request, item_id):
#         # Здесь должен быть ваш код
#         try:
#             document = json.loads(request.body)
#             resp = self.get_item(item_id, document)
#
#             return JsonResponse(resp, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({}, status=400)
#         except ObjectDoesNotExist:
#             return JsonResponse({}, status=404)
#
#     @staticmethod
#     def get_item(item_id, document):
#         # Throws Exception if item_id does not exist
#         # Does not check validity of the doc
#         # item = Item.objects.get(id=item_id)
#         # reviews = Review.objects.filter(item=item).order_by('-id')[:5]
#         schema = ItemSchema()
#         return {
#             'id': item.id,
#             'title': item.title,
#             'description': item.description,
#             'price': item.price,
#             'reviews': reviews
#         }

"""
    Marshmallow variant 
"""
import json

from django.contrib.auth import authenticate

from django.http import HttpResponse, JsonResponse
from django.views import View

from django.utils.decorators import method_decorator

from marshmallow import Schema, ValidationError, fields, post_load
from marshmallow.validate import Length, Range

from .models import Item, Review

from functools import wraps


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=Length(1, 64))
    description = fields.Str(required=True, validate=Length(1, 1024))
    price = fields.Int(required=True, validate=Range(1, 1000000), strict=True)

    @post_load
    def make(self, data):
        return Item(**data)


class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    grade = fields.Int(required=True, validate=Range(1, 10), strict=True)
    text = fields.Str(required=True, validate=Length(1, 1024))

    @post_load
    def make(self, data):
        return Review(**data)


def staff_required(view_func):
    """ Decorator checks if user has flag 'is_staff' """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            view_func(request, *args, **kwargs)
        else:
            return HttpResponse(status=403)

    return _wrapped_view


def basic_auth(view_func):
    """ Defines HTTP BASIC AUTH """

    import base64

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION'):
            auth = request.META.get('HTTP_AUTHORIZATION').split()
            if len(auth) == 2 and auth[0].lower() == 'basic':
                username, password = base64.b64decode(auth[1]).split(':')  # decode('utf-8')
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    request.user = user
                    return view_func(request, *args, **kwargs)
        return HttpResponse(status=401)

    return _wrapped_view


@method_decorator(basic_auth, name='dispatch')
@method_decorator(staff_required, name='dispatch')
class AddItemView(View):
    """View РґР»СЏ СЃРѕР·РґР°РЅРёСЏ С‚РѕРІР°СЂР°."""

    def post(self, request):
        try:
            document = json.loads(request.body)
            schema = ItemSchema(strict=True)
            item = schema.load(document).data
            item.save()
        except (json.JSONDecodeError, ValidationError, AssertionError):
            return HttpResponse(status=400)
        data = {'id': item.pk}
        return JsonResponse(data, status=201)


class PostReviewView(View):
    """View РґР»СЏ СЃРѕР·РґР°РЅРёСЏ РѕС‚Р·С‹РІР° Рѕ С‚РѕРІР°СЂРµ."""

    def post(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            document = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            review = schema.load(document).data
            review.item = item
            review.save()
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        except (json.JSONDecodeError, ValidationError):
            return HttpResponse(status=400)
        data = {'id': review.pk}
        return JsonResponse(data, status=201)


class GetItemView(View):
    """View РґР»СЏ РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё Рѕ С‚РѕРІР°СЂРµ.

    РџРѕРјРёРјРѕ РѕСЃРЅРѕРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё РІС‹РґР°РµС‚ РїРѕСЃР»РµРґРЅРёРµ РѕС‚Р·С‹РІС‹ Рѕ С‚РѕРІР°СЂРµ, РЅРµ Р±РѕР»РµРµ 5
    С€С‚СѓРє.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        schema = ItemSchema()
        data = schema.dump(item).data
        query = Review.objects.filter(item=item).order_by('-id')
        reviews = query[:5]
        schema = ReviewSchema(many=True)
        data['reviews'] = schema.dump(reviews).data
        return JsonResponse(data, status=200)
