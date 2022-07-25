from blog_app.models import users,posts

session={}

def signin_required(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("invalid")
    return wrapper

def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user=[user for user in users if user["username"]==username and user["password"]==password]
    return user

class SignInView():
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            print("login success")
            session["user"]=user[0]
        else:
            print("invalid credentials")

class PostListView():
    def get(self,*args,**kwargs):
        return posts
    def post(self,*args,**kwargs):
        user_id=session["user"]["id"]
        kwargs["userId"]=user_id
        print(kwargs)
        posts.append(kwargs)
        print(posts)

class MyPostView():
    def get(self,*args,**kwargs):
        user_id=session["user"]["id"]
        my_post=[post for post in posts if post["userId"]==user_id]
        return my_post

class PostDetailsView():
    def get_object(self,id):
        post=[post for post in posts if post["postId"]==id]
        return post

    def get(self,*args,**kwargs):
        postid=kwargs.get("postid")
        posts=self.get_object(postid)
        return posts

    def delete(self,*args,**kwargs):
        postid=kwargs.get("postid")
        data=self.get_object(postid)
        if data:
            post=data[0]
            posts.remove(post)
            print("post removed")
            print(posts)
            return post
    def put(self,*args,**kwargs):
        post_id=kwargs.get("post_id")
        data=kwargs.get("data")
        value=self.get_object(post_id)
        if value:
            post=value[0]
            post.update(data)
            return post

class LikeView():
    def get(self,*args,**kwargs):
        post_id=kwargs.get("post_id")
        post=[post for post in posts if post["postId"]==post_id]
        if post:
            post=post[0]
            user_id=session["user"]["id"]
            post["liked_by"].append(user_id)
            print(post)

def signout(*args,**kwargs):
    session.pop("user")
    username=user["username"]



login=SignInView()
login.post(username="anu",password="Password@123")

all_posts=PostListView()
print(all_posts.get())

all_posts.post(postId=9,title="Hey all of you",content="how are you guys?",liked_by=[])

my_post=MyPostView()
print(my_post.get())

postdetails=PostDetailsView()
print(postdetails.get(postid=6))
print(postdetails.delete(postid=7))
data={
    "title":"swetha"
}
print(postdetails.put(post_id=4,data=data))

like=LikeView()
like.get(post_id=1)

