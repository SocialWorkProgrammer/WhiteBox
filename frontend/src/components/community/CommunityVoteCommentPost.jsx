import React, { useState } from 'react';
import { useCommunityStore } from '../../store/useCommunityStore';
import lawyerBadge from '../../public/img/lawyerBadge.png'

const CommunityGeneralCommentPost = ({ id, onCommentUpdate }) => {
  const user = localStorage.getItem('user')
  const userJson = user? JSON.parse(user) : null;
  const userId = userJson.nickname
  const isLawyer = userJson.isLawyer
  const [comment, setComment] = useState('');
  const postCommunityComment = useCommunityStore((state) => state.postVoteComment);
  const getCommunityVoteDetail = useCommunityStore((state) => state.getCommunityVoteDetail);

  const handleCommentChange = (e) => {
    setComment(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!comment.trim()) {
      return alert('댓글을 입력하세요');
    }

    try {
      // 댓글을 포스트하고 새로운 댓글 데이터 가져오기
      const newComment = await postCommunityComment({ id, comment });
      if (newComment.status === 200) {
        console.log('댓글이 추가되었다!!!', newComment.status);
        const response = await getCommunityVoteDetail({ voteId : id });
        console.log('asdfasdf', response.comments)
        onCommentUpdate(response.comments, Math.ceil(response.comments.length));
      }
      setComment(''); // 댓글 작성 후 입력란 초기화
    } catch (error) {
      console.error('댓글 작성 중 오류 발생:', error);
    }
  };
  const handleKeyDown = (event) => {
    if (event.key === 'Enter' & !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event)
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col space-y-2 w-[100%] border-2 rounded">
      <div className="flex flex-row place-content-between w-[100%] border-b-2">
        <div className="flex flex-row items-center gap-3">
          {isLawyer === true ?  <img src={lawyerBadge} alt="" className="h-8 w-8" /> : <div className="h-8 w-8"></div>}
          <p className="">{userId}</p>
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white p-2 hover:bg-blue-600"
        >
          댓글 작성
        </button>
      </div>
      <textarea
        value={comment}
        onChange={handleCommentChange}
        onKeyDown={handleKeyDown}
        placeholder="댓글을 작성하세요."
        className="rounded p-2 w-[100%]"
        rows="4"
      />
    </form>
  );
};

export default CommunityGeneralCommentPost;
