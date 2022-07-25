from blog_app.models import users,posts

def signin_required(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
    return wrapper


session={}

# "and" and "&" difference:
#and: koduthal oru side check cheythit false aanel aduthathilek povilla false print aavum
#&:  koduthal oru side false aanelium another  side check cheyth falsum falsum compare cheyan nikum

def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user = [user for user in users if user["username"] == username and user["password"] == password]
    return user


#get==>retrieve
#post===>create
#put/patch===>update/edit
#Delete==>delete

class SignInView:
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)  #authenticate ivideyaan call cheyende
        if user:
            print("success")
            session["user"]=user[0]   #user[0]: list kalayan vendeet, #session : key=user,value=full details of user
                                     #session oru dic aan so key and values aan add cheynne
        else:
            print("invalid")


class PostView():    #ella postum view cheyan  ,post create cheyan ulla function
    @signin_required
    def get(self,*args,**kwargs):
        return posts
    @signin_required
    def post(self,*args,**kwargs):
        userId=session["user"]["id"]
        kwargs["userId"]=userId
        print(kwargs)
        posts.append(kwargs)
        print("post added")
        print(posts)

class MyPostView():
    @signin_required
    def get(self,*args,**kwargs):
        userId=session["user"]["id"]
        my_post=[post for post in posts if post["userId"]==userId]
        return my_post


login=SignInView()
login.post(username="anu",password="Password@123")

class PostDetailsViews:  #specific post list cheyan,update cheyan,delete cheyan elam kude ithil

    @signin_required
    def get_object(self,id):            #code duplicate aavathirikan kodukunu
        post=[post for post in posts if post["postId"]==id]  #nammal kodukkunna id ulla posine return cheyua
        return post
    @signin_required
    def get(self, *args, **kwargs):   #specific post list cheyan
        post_id = kwargs.get("post_id")
        post=self.get_object(post_id)
        return post
    @signin_required
    def delete(self,*args,**kwargs):   #delete cheyan
        post_id=kwargs.get("post_id")
        data=self.get_object(post_id)
        if data:
            post=data[0]  #list[dic] kalatan aan [0]
            posts.remove(post)
            print("post removed")
            print(len(posts))  #len nokiyal remove aayo ariyan

    @signin_required
    def put(self,*args,**kwargs):
        post_id=kwargs.get("post_id")
        data=kwargs.get("data")
        value=self.get_object(post_id)
        if value:
            post=value[0]
            post.update(data)


        return post
@signin_required
class LikeView:
    def get(self,*args,**kwargs):
        post_id=kwargs.get("post_id")
        post=[post for post in posts if post["postId"]==post_id]
        if post:
            post=post[0]
            userid=session["user"]["id"]
            post["liked_by"].append(userid)
            print(post)

def signout(*args,**kwargs):
    user=session.pop("user")
    username=user["username"]
    print(f"the user {username}  has been logged out")   #fstring
    #now="ekm"
    #frm="tvm"
    #name="ajay"

    #fstring: print(f"hai all am {name} from {frm} at present am in {now}


# data=PostView()
# print(data.get())
# data.post(post_id=9,title="Hello",content="Goodmorning all of you",liked_by=[])

myposts=MyPostView()
print(myposts.get())

# post_details=PostDetailsViews()
# post_details.delete(post_id=6)
# print(post_details.get(post_id=5))
#
# data={
#     "title":"new title"
# }
#
# print(post_details.put(post_id=5,data=data))             #put method use cheyumbo rand karyanghal aan pass cheyende
                                #eth resource aan uodate cheyende: ndhaan update cheyende


like=LikeView()
like.get(post_id=4)
signout()
