import CommunityVoteTabs from "./CommunityVoteTabs";
import { useEffect, useState } from "react";
import CommentImg from '../../public/img/comment.svg'
import axios from "axios";
import { useCommunityStore } from '../../store/useCommunityStore'
import Pagination from './CommunityPagination'
import blankImage from '../../public/img/blank-image.svg'
import dayjs from 'dayjs'
import VoteGraph from './CommunityVoteGraph'
import { useParams, useNavigate } from "react-router-dom";
import CommentPostForm from './CommunityVoteCommentPost'
import VoteCommentDeleteButton from '../buttons/VoteCommentDeleteButton'
import { Helmet } from 'react-helmet';
import lawyerBadge from '../../public/img/lawyerBadge.png'


function CommunityGeneralDetail() {
  const storedUser = localStorage.getItem ? JSON.parse(localStorage.getItem('user')) : null;
  const isLawyer = storedUser.isLawyer
  // 게시글 정보 가져오기 
  const voteId = useParams().id;
  const  [data, setData] = useState({
    aiOtherFault : 0,
    aiRelatedInformation : '',
    aiRelatedLaw: '',
    aiUserFault: 0,
    approvalPercent: 0,
    comments: [],
    commentsCount: 0,
    createdAt: '',
    description: '',
    hit: '',
    isimage: '', //data에서는 isimage가 아닌 image로 나오므로 주의!
    images: [],
    neutralPercent: 0,
    oppositePercent: 0,
    title: '',
    video: '', //data에서는 videoUrl로 나오므로 주의!
    voteId: 0,
    votesCount: 0,
  });
  const [error, setError] = useState(null);
  
  // 댓글 정보 가져오기(페이지네이션)
  const getCommunityVoteDetail = useCommunityStore((state) => state.getCommunityVoteDetail); // 게시판 목록 불러오기
  const [currentPage, setCurrentPage] = useState(1); // 현재 페이지와, 이동할 페이지, default 값은 1
  const [itemsPerPage] = useState(10); // 한 페이지에 들어갈 아이템의 수
  
  useEffect(() => {
    const loadCommunityCommentList = async () => {
        try {
          const response = await getCommunityVoteDetail({voteId});
          const date = dayjs(response.createdAt).format('YYYY-MM-DD HH:mm:ss');
          console.log('요청받은 데이터 = ', response);
          setData({
            aiOtherFault : response.aiOtherFault,
            aiRelatedInformation : response.aiRelatedInformation,
            aiRelatedLaw: response.aiRelatedLaw,
            aiUserFault: response.aiUserFault,
            approvalPercent: response.approvalPercent,
            comments: response.comments,
            commentsCount: response.commentsCount,
            createdAt: date,
            description: response.description,
            hit: response.hit,
            isimage: response.image, //data에서는 isimage가 아닌 image로 나오므로 주의!
            images: response.images,
            neutralPercent: response.neutralPercent,
            oppositePercent: response.oppositePercent,
            title: response.title,
            video: response.video, //data에서는 videoUrl로 나오므로 주의!
            voteId: response.voteId,
            votesCount: response.votesCount,
            })  
          // 여기서 setData(가공된 responseData)를 통해서 데이터설정을 해주세용
        } catch (err) {
          console.log(err);
          throw err
        }
      }
      loadCommunityCommentList();
  }, [getCommunityVoteDetail, voteId]);


  // 페이지네이션 관련 변수들
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = data.comments.length > 0 ? data.comments.slice(indexOfFirstItem, Math.min(data.comments.length, indexOfLastItem)) : [];
  const handlePageChange = (page) => {
    setCurrentPage(page);
  }

  // 댓글 작성 시 새로고침 기능
  const handleCommentUpdate = (newComments, lastComment) => {
    console.log('받은 new 투표댓글들=', newComments);
    setData((prevData) => ({
      ...prevData,
      comments: newComments,
    }));
    console.log('alsdfjl;asdjfk', data.comments);
    setCurrentPage(Math.ceil(lastComment/10));
  };

        
  return (
    <div>
      <Helmet>
        <title>White box | 투표게시판 | {data.title}</title>
      </Helmet>
      <CommunityVoteTabs className="col-span-8"/>
      <div className="grid grid-cols-12 min-h-[300px]">
        <div className="col-span-2"></div>
        {/* 여기서부터 글 컨테이너 */}
        <div className="max-w-[1300px] col-span-8 flex place-content-center">
          <div className= "h-auto border-x-2">
            <div className="flex border-box min-h-[34px] px-[7px] p-1 bg-[#BBBBBB]"><p className="text-xl">{data.title}</p></div>
              <div className="border-box grid grid-cols-12 text-[15px] mt-2">
                <div className="col-span-8 ml-2">{data.nickname}</div>
                <div className="col-span-4 flex flex-row">
                  <span className="">투표 수</span>
                  <span className="text-[#231FE8]">{data.hit}</span>
                  <span className="mx-2">|</span>
                  <span className="">작성일 {data.createdAt}</span>
                </div>
              </div>
            {/* 내용 */}
            <div className="min-h-[300px] p-3">
              {/* 비디오 */}
              <div className="flex flex-row place-content-between">
                <video controls width="500" 
                  src={data.video}></video>
                <div>
              {/* 현장사진 */}
                <p>현장사진</p>
                <div className="grid grid-cols-2 gap-4 max-w-[700px] max-h-[400px] m-2">
                {data.images.map((image, idx) => (
                  <img
                  key={idx}
                  // src={image.image}
                  src={`${blankImage}`}
                  alt='#'
                  // 스마트폰 사진비율 16:9에 맞춤
                  className= "w-[304px] h-[171px]"
                  />
                )) }
              </div>
                </div>
              </div>
              <p className="min-h-[30px] font-normal mt-10">{data.description}</p>
            </div>
            {/* 투표 */}
            <VoteGraph
              voteId = {voteId}
              approvalPercent = {data.approvalPercent}
              neutralPercent = {data.neutralPercent}
              oppositePercent = {data.oppositePercent}
              className=""
              />
              <div>총 투표 수 : {data.votesCount}</div>
            {/* 댓글 영역 */}
            <div className="w-auto h-[73px] border-y-2 my-4 flex align-middle">
              <img 
                src={CommentImg}
                alt=""
                className="pl-7"
              />
            </div>
            {/* 댓글 */}
            <div className="space-y-1 px-2 pb-3 pt-2">
            <CommentPostForm id={voteId} onCommentUpdate={handleCommentUpdate} />
            {currentItems.length > 0 ? (
            currentItems.map((comment, idx) => {
                const commentDate = dayjs(comment.postedAt).format('YYYY-MM-DD HH:mm:ss')
                return (
                <div key={idx} className="flex flex-col h-[95px] border-b-2">
                <div className="flex flex-row justify-between">
                <div className="flex flex-row gap-3">
                  {isLawyer === true ?  <img src={lawyerBadge} alt="" className="h-8 w-8" /> : <div className="h-8 w-8"></div>}
                  <div className="border-box text-xl">{comment.userNickname}</div>
                  </div>
                  <div className="justify-self-end col-span-3 text-xl">{commentDate}</div>
                </div>
                <div className="mt-4">{comment.comment}</div>
                </div>)
              })): (
              <p>댓글 없음!</p>
            )
          }
            </div>
            <Pagination
            totalItems={data.comments.length}
            itemsPerPage={itemsPerPage}
            currentPage={currentPage}
            onPageChange={handlePageChange}
            className="relative w-auto"
            />

          </div>
        <div className="col-span-2"></div>
      </div>
    </div>
    </div>
  )
}

export default CommunityGeneralDetail;