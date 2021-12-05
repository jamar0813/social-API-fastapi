from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from .. import schemas, models, database, oauth2

router = APIRouter(
    prefix= '/vote',
    tags= ['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # create query to find post
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    # create query to find vote
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    #verify that post exits
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Post with id {vote.post_id} does not exists'
        )
    #check to see if the is a vote or if the value is 0
    elif (vote.dir == 1):
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail = f'user {current_user.id} has already voted on post {vote.post_id}'
            )

        #create the vote    
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully Voted!"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= f'Vote does not exist'
            )

        # delete the vote    
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Vote Deleted!"}