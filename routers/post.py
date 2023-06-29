from .. import models,schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix = '/posts',
    tags = ['Posts']
)


@router.get('/', response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return {"data": posts}
    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # return {"data": post_dict}
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data": new_post}
    # new_post = models.Post(title = post.title, content = post.content, published = post.published) # if there are 50 coumns, then it is inefficient to write all 50 attributes in this way.
    new_post = models.Post(**post.dict()) # its good to just unpack all the attributes from the dict
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model = schemas.Post)
def get_post(id: int, response: Response,db: Session = Depends(get_db)):
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id {id} was not found')
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {'message': f'post with id {id} was not found'}
    # return {"post": post}
    # cursor.execute(f"""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id {id} was not found')
    # return {"data": post}
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id {id} was not found')
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f" post with {id} is not present")
    # my_posts.pop(index)
    # return Response(status_code = status.HTTP_204_NO_CONTENT)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id {id} was not found')
    # return {"data": post}
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id {id} was not found')
    post.delete(synchronize_session = False)
    
    db.commit()
    

    return {"status_code": status.HTTP_204_NO_CONTENT}

     

@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # index = find_index_post(id)

    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f" post with {id} is not present")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # return {"data": post_dict}
    # cursor.execute("""UPDATE posts SET title =%s, content = %s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    # if post == None:
    #         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f" post with {id} is not present")

    # return {"data" : post} 
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f" post with {id} is not present")

    post_query.update(updated_post.dict(), synchronize_session = False)

    db.commit()

    return post_query.first()