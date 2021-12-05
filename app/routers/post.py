from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix = '/posts',
    tags = ['Posts']
)

# Get all posts in the database
# next steps is to add pagination for performance 
@router.get('/', response_model=List[schemas.PostResponseVotes])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, 
skip: int = 0, search: Optional[str] = ''):

    #This grabs all post as long as the user is signed in
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # results = db.query(models.Post, func.count(models.Votes.post_id).label('votes')).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # This would grab only all the post created by the user
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    # posts = db.query(models.Post).all()

    return posts

# Create a post in the database
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #new_post = models.Post(
    #    title = post.title,
    #    content = post.content,
    #    published = post.published
    #)
    # this is more efficient method that will expand if we add columns to the model

    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# Get a post by id from database
@router.get('/{id}', response_model=schemas.PostResponseVotes)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #post = db.query(models.Post).filter(models.Post.id == id).one_or_none()
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).one_or_none()

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'Post with id: {id} not found'
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'Post with id: {id} not found'}

    return post

# delete a post in the database by id
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Run the query to grabe the post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # Grab the fist post for checking if exist and user id
    post = post_query.first()

    if post ==None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'Post with id: {id} not found'
        )
    elif post.user_id != current_user.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= f'Not authorized to perform requested action'
        )
    else:
        post_query.delete(synchronize_session=False)
        db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# this will update data in the database
@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query =db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()

    if post ==None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'Post with id: {id} not found'
        )
    elif post.user_id != current_user.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= f'Not authorized to perform requested action'
        )
    else:
        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()

    return post_query.first()