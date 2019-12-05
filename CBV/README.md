## CVB调研

### CBV和FBV的差别

- FBV : function base views, 就是在视图里使用函数处理请求

  ```python
  def index(request):
      if request.method == 'GET':
          return JsonResponse({'code': 200})
  
  ```

- class-based views 

  ````python
  class HelloView(View):
  	def get(self, request):
  		return JsonResponse({'code':200})
  ````

### View方法的调用顺序

1. 装饰器会优先于view内函数,所以将权限判断放在装饰器中调用

2. ​	__   init   __()

   - 将路由中的正则匹配内容 存入类中的kwargs字典中 ;   获取: self.kwargs[“mobile”]

3.   as_view ［入口］

   - 装饰器封装了属性view_class和view_initkwargs 和功能view()  
   - 把request以及参数封装传递给了Class.dispatch，然后调用Class.dispatch

   - 请求的request数据获取

4. dispatch   ［分发］

   - 它从request.method中获取请求类型(假设是GET)，并进行反射，并交给我们在Class中写好的对应方法(GET)去执行.那么dispatch就相当于一个请求分发器，它在请求处理前执行

   ```python
   def dispatch(self, request, *args, **kwargs):
       # Try to dispatch to the right method; if a method doesn't exist,
       # defer to the error handler. Also defer to the error handler if the
       # request method isn't on the approved list.
       if request.method.lower() in self.http_method_names:
           handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
       else:
           handler = self.http_method_not_allowed
           return handler(request, *args, **kwargs)
   ```

5. http_method_not_allowed　　［前端大黄页］

6. _allowed_methods

   - 用列表迭代器，返回请求方法的名字

7. options　［请求方法］









```

```

