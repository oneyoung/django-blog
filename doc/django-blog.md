# Setup BLog with Django

### 建立一个project
首先, 确保你的系统已经安装好`Django`.

然后, 运行如下命令建立project:
```bash
django-admin.py startproject blog
```
就会生成如下目录结构:
```
.
|-- blog
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
`-- manage.py

1 directory, 5 files
```
在本地运行测试服务器:
```bash
./manage.py runserver
```
会在本地监听8000端口, 可以通过`http://127.0.0.1:8000/`访问.
```
Validating models...

0 errors found
Django version 1.4.3, using settings 'blog.settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### setting.py 设置
这里主要是数据库的设置, 最简单的就是选"sqlite3".

> If you're using SQLite, the database will be a file on your computer; in that case, NAME should be the full absolute path, including filename, of that file. If the file doesn't exist, it will automatically be created when you synchronize the database for the first time (see below).

根据文档, 选择`sqlite3`模式, 会直接把一个文件当成数据库, 把`NAME`指向文件绝对路径, 其他都不用设置了.

使用绝对路径时候, 这里就有一个问题了, 有时候项目文件路径经常会换. 比如你是在自己PC开发的, 最后再上传到服务器, 就要改绝对路径, 这不科学. 所以可以在setting.py里做个手脚, 反正是python 文件, 可以自由发挥:
```python
import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
abspath = lambda rel: os.path.join(PROJECT_ROOT, rel)
```

最后的配置就是这样:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': abspath('db/sqlite3.db'),  # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
```

其他:
```python
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'utf-8'
MEDIA_ROOT = abspath('media/')
MEDIA_URL = '/media/'
STATIC_ROOT = abspath('static/')
STATIC_URL = '/static/'
```

### project 改名
遇到一个坑爹的问题, Django 要修改project name 似乎很困难, 没有内置支持的命令, 只能人肉.

比如要将`blog`改为`blogsite`.  grep 一下, 泥玛一堆命中:
```bash
$ find -name "*.py" -exec grep -r "blog" {} \;
manage.py:    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
blog/settings.py:# Django settings for blog project.
blog/settings.py:ROOT_URLCONF = 'blog.urls'
blog/settings.py:WSGI_APPLICATION = 'blog.wsgi.application'
blog/urls.py:    # url(r'^$', 'blog.views.home', name='home'),
blog/urls.py:    # url(r'^blog/', include('blog.foo.urls')),
blog/wsgi.py:WSGI config for blog project.
blog/wsgi.py:os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
```
好在现在还刚开始, 直接用`sed` 替换掉
```bash
mv blog blogsite
find -name "*.py" -exec sed -i -e "s/\<blog\>/blogsite/g" {} \\;
```

### 建立并激活models
#### 新建一个app:
```bash
./manage.py startapp blog
```
就会建立如下目录结构:
```
blog
|-- __init__.py
|-- models.py
|-- tests.py
`-- views.py
```
然后就可以在`models.py`建立自己的数据模型, 具体文档可以猛击[这里](https://docs.djangoproject.com/en/1.4/topics/db/models/).

#### 激活model
在`setting.py` 里有一个`INSTALLED_APPS`, 把我们刚建立的app加进去:
```python
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'blog',
)
```
然后, 需要运行`syncdb`确保数据库已被建立:
```bash
./manage.py syncdb
```

### 模板
####基本语法
* *block tag* - 在`{%`和`%}` 之间, 可以内嵌一些处理语句: <br />
  `{% if is_logged_in %}Thanks for logging in!{% else %}Please log in.{% endif %}`
* *variable* - `{{` `}}`, 变量替换, 和`"%s" % varialbe`差不多: <br />
  ` My first name is {{ first_name }}. My last name is {{ last_name }}.`
	* 变量名有也可以用`.`实现成员查找: <br />
	  对于`foo.bar`, 查找会依照下面顺序 <br />
		* Dictionary lookup. Example: foo["bar"]
		* Attribute lookup. Example: foo.bar
		* List-index lookup. Example: foo[bar]

