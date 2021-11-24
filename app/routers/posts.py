from sqlalchemy.sql.functions import count
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.get("/", response_model= List[schemas.PostVotes])
#@router.get("/", )
def get_posts(db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user), limit: int =10, skip: int = 0, search: Optional[str] = ""):
   # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
 #       posts = db.query(models.Post).filter(models.Post.owner_id ==current_user_id.id).all()
#    cursor.execute(""" SELECT * FROM posts """)
#    posts = cursor.fetchall()
    return posts

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{"data": posts}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
  #  new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id = current_user_id.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #sanitizes the inputs, not vulrenable to sql injections
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
 #   post_dict = post.dict()
 #   post_dict['id'] = randrange(1,1000000)
 #   my_posts.append(post_dict)
 #   return {"data":post_dict}.
    return new_post

#get latest post (only works if the routes of "/posts/{id}" have a different variable before the {id})
#or if the delete comes before the others with the {id} variable in the code.
#path parameters work up - down
@router.get("/{id}", response_model= schemas.PostVotes)
def get_post(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
#   print(id)
#    post  = printpost(id)
    # cursor.execute("""SELECT * FROM posts WHERE ID=%s""",(str(id),))
    # this_post = cursor.fetchone()
    #this_post = db.query(models.Post).filter(models.Post.id==id).first()
    this_post = db.query(models.Post, count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id==id).first()

    # db.query(models.Post, count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(
    #         models.Post.id).filter(models.Post.title.all()
    if not this_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}'''
    #print(type(id))
    return  this_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
  #  index = indexposts(id)
    # cursor.execute("""DELETE from posts WHERE id=%s RETURNING *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    print(post)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"status with the id:{id} not found")
    if post.owner_id != current_user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Can't delete other users' posts")

    post.delete(synchronize_session=False)
    db.commit()
 #   my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int,post_sc: schemas.PostCreate, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
 #   index = indexposts(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"status with the id:{id} not found")
    
    if post.owner_id != current_user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Can't update other users' posts")
    
    post_query.update(post_sc.dict(), synchronize_session= False)
    db.commit()
 #   post_dict=post.dict()
 #   post_dict["id"] = id
 #   my_posts[index] = post_dict
    return post_query.first()