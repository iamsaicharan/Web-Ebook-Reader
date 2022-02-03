# from django.views import ListView
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import Paginator
from analytics.models import ObjectViewedMixin
from django.db.models import Q

# Create your views here.
from .models import Product
import os
import functools
import hashlib
import shutil
import urllib
import zipfile
import glob
import re
import random
import xml.sax.handler
from xml.etree import ElementTree
from lxml import objectify
from xml.dom import minidom
import codecs
from bs4 import BeautifulSoup
from library.models import Library

def xml2obj(src):
    non_id_char = re.compile('[^_0-9a-zA-Z]')

    def _name_mangle(name):
        return non_id_char.sub('_', name)

    class DataNode(object):
        def __init__(self):
            self._attrs = {}    # XML attributes and child elements
            self.data = None    # Child text data

        def __len__(self):
            # Treats single element as a list of 1
            return 1

        def __getitem__(self, key):
            if isinstance(key, str):
                return self._attrs.get(key,None)
            else:
                return [self][key]

        def __contains__(self, name):
            return self._attrs.has_key(name)

        def __nonzero__(self):
            return bool(self._attrs or self.data)

        def __getattr__(self, name):
            if name.startswith('__'):
                raise AttributeError(name)
            return self._attrs.get(name,None)

        def _add_xml_attr(self, name, value):
            if name in self._attrs:
                # Multiple attributes of the same name are represented by a list
                children = self._attrs[name]
                if not isinstance(children, list):
                    children = [children]
                    self._attrs[name] = children
                children.append(value)
            else:
                self._attrs[name] = value

        def __str__(self):
            return self.data or ''

        def __repr__(self):
            items = sorted(self._attrs.items())
            if self.data:
                items.append(('data', self.data))
            return u'{%s}' % ', '.join([u'%s:%s' % (k,repr(v)) for k,v in items])

    class TreeBuilder(xml.sax.handler.ContentHandler):
        def __init__(self):
            self.stack = []
            self.root = DataNode()
            self.current = self.root
            self.text_parts = []

        def startElement(self, name, attrs):
            self.stack.append((self.current, self.text_parts))
            self.current = DataNode()
            self.text_parts = []
            # XML attributes to Python attributes
            for k, v in attrs.items():
                self.current._add_xml_attr(_name_mangle(k), v)

        def endElement(self, name):
            text = ''.join(self.text_parts).strip()
            if text:
                self.current.data = text
            if self.current._attrs:
                obj = self.current
            else:
                # Text only node is simply represented by the string
                obj = text or ''
            self.current, self.text_parts = self.stack.pop()
            self.current._add_xml_attr(_name_mangle(name), obj)

        def characters(self, content):
            self.text_parts.append(content)

    builder = TreeBuilder()
    # TODO: Handle exceptions
    if isinstance(src, str):
        xml.sax.parseString(src, builder)
    else:
        xml.sax.parse(src, builder)
    values = list(builder.root._attrs.values())
    return values[0]

def find_between(s, first, last):
        """
        Help methods for parsing NCX files, finds first sub-string between two strings
        :param s: String to search in
        :param first: First sub-string
        :param last: Second sub-string
        :return: Sub-string from given string between first and second sub-string
        """
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

@method_decorator(login_required, name='dispatch')
class ProductFeaturedListView(ListView):
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()

@method_decorator(login_required, name='dispatch')
class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/featured-detail.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()

@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        products = Product.objects.all()
        paginator = Paginator(products, 30)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        print(page.paginator.page_range)
        print(len(products))
        return page.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        products = Product.objects.all()
        paginator = Paginator(products, 30)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        if page.has_next():
            next_url = f'?page={page.next_page_number()}'
        else:
            next_url = ''

        if page.has_previous():
            prev_url = f'?page={page.previous_page_number()}'
        else:
            prev_url = ''

        print(page.paginator.page_range)
        print(len(products))
        context["page"] = page
        context["next_page_url"] = next_url
        context["prev_page_url"] = prev_url
        return context

@method_decorator(login_required, name='dispatch')
def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)

@method_decorator(login_required, name='dispatch')
class ProductDetailView(ObjectViewedMixin, DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        request = self.request
        library_obj, new_obj = Library.objects.new_or_get(request)
        context['library'] = library_obj
        print(context)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')

        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404('Product do not exist')

        return instance

@method_decorator(login_required, name='dispatch')
def product_detail_view(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk)
    # instance = get_object_or_404(Product, pk=pk)
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('no product here')
    #     raise Http404('Product do not exist')
    # except:
    #     print('huh?')

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404('Product do not exist')
    # print(instance)
    # qs = Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404('Product do not exist')


    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)

@method_decorator(login_required, name='dispatch')
class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

@method_decorator(login_required, name='dispatch')
class CategoryView(ListView):
    template_name = 'products/category_view.html'
    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            lookups = Q(category=query)
            return Product.objects.filter(lookups).distinct()
        else:
            return Product.objects.none()

@login_required
def Reader(request, pk=None, *args, **kwargs):
    instance = get_object_or_404(Product, pk=pk)
    handle = zipfile.ZipFile(instance.ebook)
    folder_name = random.randint(0, 646421467976464)
    folder_unzip = os.path.join(settings.MEDIA_ROOT, 'temp')
    delfold = glob.glob(folder_unzip + '\\')
    for f in delfold:
        filepathrem = os.path.join(folder_unzip, f)
        shutil.rmtree(f)
    # pathname = folder_unzip + '\\' + str(folder_name) + '\\'
    pathname = folder_unzip + '/' + str(folder_name) + '/'
    print(pathname)
    handle.extractall(pathname)
    container_data = xml2obj(open((pathname + "META-INF/container.xml"), "r", encoding="utf8"))
    opf_file_path = container_data.rootfiles.rootfile.full_path
    get_metadata = xml2obj(open(os.path.join(pathname, opf_file_path), 'r', encoding="utf8"))
    get_oebps = os.path.split(opf_file_path)[0]
    for x in get_metadata.manifest.item:
        if x.media_type == "application/x-dtbncx+xml":
            get_ncx_file_path = os.path.join(pathname, get_oebps, x.href)
    ncxPath = get_ncx_file_path.split('\\')[:-1]
    pathncx = ''
    for obj in ncxPath:
        pathncx = pathncx + str(obj) + '/'
    new_get_ncx_file_path = ncxPath
    files= []
    for x in get_metadata.manifest.item:
        if x.media_type == "application/xhtml+xml":
            files.append(x.href)
    stylefiles= []
    for x in get_metadata.manifest.item:
        if x.media_type == "text/css":
            stylefiles.append(x.href)
    removefiles = []
    for x in get_metadata.manifest.item:
        if x.id == "cover":
            removefiles.append(x.href)
    for x in get_metadata.manifest.item:
        if x.id == 'titlepage':
            removefiles.append(x.href)
    for x in get_metadata.manifest.item:
        if x.id == 'about':
            removefiles.append(x.href)
    for x in get_metadata.manifest.item:
        if x.id == 'feedbooks':
            removefiles.append(x.href)
    for x in get_metadata.manifest.item:
        if x.id == 'footnotes':
            removefiles.append(x.href)
    removepaths = []
    for obj in removefiles:
        filepath = pathncx + obj
        removepaths.append(filepath)
    pathdic = []
    for obj in files:
        filepath = pathncx + obj
        pathdic.append(filepath)
    finalpath = [x for x in pathdic if x not in removepaths]
    context = {
         'path': finalpath,
    }
    return render(request, 'products/reader.html', context)