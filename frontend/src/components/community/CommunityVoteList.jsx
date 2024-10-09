import React, {useEffect, useState} from 'react';
import "../../styles/community/communitygenrallist.css"
// 다른 컴포넌트 가져오기
import Pagination from "./CommunityPagination";
import WriteButton from '../buttons/WriteButton';
import CommunityGeneralCreate from './CommunityGeneralCreate'
import CommunityVoteTabs from './CommunityVoteTabs';
// Store 불러오기
import { useCommunityStore } from '../../store/useCommunityStore';
import ImageSlider from '../community/CommunityVoteImageSlider'
import hotvotepost from '../../public/img/hotvotepost.svg'
import { Helmet } from 'react-helmet';
import { formatDistanceToNow, parseISO, differenceInDays, differenceInHours, differenceInMinutes } from "date-fns";


function CommunityGeneralList() {
  const getCommunityVoteList = useCommunityStore((state) => state.getCommunityVoteList); // 게시판 목록 불러오기
  const [data, setData] = useState([]);
  const [totalElements, setTotalElements] = useState() // 총 게시물 수
  const [currentPage, setCurrentPage] = useState(1); // 현재 페이지와, 이동할 페이지, default 값은 1
  const [itemsPerPage] = useState(10); // 한 페이지에 들어갈 아이템의 수
  
  useEffect(() => {
    const loadCommunityVoteList = async () => {
        try {
          const response = await getCommunityVoteList({pageIndex : currentPage});
          // console.log('투표게시판 목록', response );
          // 여기서 setData(가공된 responseData)를 통해서 데이터설정을 해주세용
          setData(response.content || [])
          setTotalElements(response.totalElements)
          console.log(totalElements);
        } catch (err) {
          throw err
        }
      }
    loadCommunityVoteList();
  }, []);


  // 페이지네이션 관련 변수들
  const indexOfLastItem = itemsPerPage;
  const indexOfFirstItem = 0;
  const currentItems = data.length > 0 ? data.slice(indexOfFirstItem, Math.min(indexOfLastItem, indexOfFirstItem + data.length)): [];
  const handlePageChange = (page) => {
    setCurrentPage(page);
  }

  // 마우스 호버 시 썸네일 동작
  const [isHovered, setIsHovered] = useState(null);

    // 시간 포매팅 - 투표 게시판
    const formatingExpirationTime = (dateString) => {
    const now = new Date();
    const expiration = new Date(dateString)

    const daysLeft = differenceInDays(dateString, now);
    const hoursLeft = differenceInHours(dateString, now);
    const minutesLeft = differenceInMinutes(dateString, now);

      if (daysLeft > 1) {
          return `D-${daysLeft}`;
      } else {
          return "종료";
      }
  }


  return (
    // 전체 컴포넌트
    <div>
      <Helmet>
        <title>White box | 투표게시판</title>
      </Helmet>
      <CommunityVoteTabs />
    <div className="grid grid-cols-12 border-b-2">
      {/* 그리드 좌측 여백 세 칸 차지 */}
      <div className="col-span-2"></div>
      {/* 여기부터 자유게시판 컴포넌트 */}
        <div className="max-w-[1300px] col-span-8 border-x-2 p-3">
          {/* 게시판 탭 */}
          {/* 게시판 */}
          <div className="mt-10 flex flex-row flex-wrap gap-5 place-content-center">
          {currentItems.length > 0 ? (
            currentItems.map((item, idx) => (
            <a
              href={`/community/vote/${item.voteId}`} 
              className="flex flex-row gap-[15px] text-xl my-2 hover:border" 
              key={item.voteId}
              onMouseEnter={()=>setIsHovered(idx)}
              onMouseLeave={()=>setIsHovered(false)}>
              {isHovered === idx ?
                <ImageSlider
                  thumbnail1={item.thumbnail1}
                  thumbnail2={item.thumbnail2}
                  thumbnail3={item.thumbnail3}
                  thumbnail4={item.thumbnail4}
                  className="relative w-[150px] h-[150px]"
                />
                 : <img src={item.thumbnail1} className="relative w-[150px] h-[150px]"/>
              }
              <div className="flex flex-col gap-3">
                <div className="w-[200px] font-bold text-ellipsis overflow-hidden whitespace-nowrap">{item.voTitle}</div>
                <div className="flex flex-row">

                  {item.totalVotes > 10 ? <img src={hotvotepost} alt="" className="pr-2" /> : <p></p>}
                  <div className="text-[15px] font-light text-[#0A3DF2]">투표 수 {item.totalVotes}</div>
                </div>
                <div className="text-[15px] w-[240px] text-ellipsis overflow-hidden whitespace-nowrap right-0 font-bold">{item.nickname}</div>
                <div className="">{formatingExpirationTime(item.expirationDate)}</div>
              </div>
            </a>
          ))): (
            <div className="col-span-6 flex flex-nowrap gap-[15px] max-w-[397px] h-[150px] border-2 text-xl items-center my-2">아직 글이 없습니다.</div>
          )}
          </div>
          <div className="relative w-auto h-[38px] mt-5 mb-10">
          </div>
          <Pagination
            totalItems={totalElements} 
            itemsPerPage={itemsPerPage}
            currentPage={currentPage}
            onPageChange={handlePageChange}
            className="relative w-auto"
            />
        </div>
      {/* 그리드 우측 여백 세 칸 */}
      <div className="col-span-3"></div>
    </div>
    </div>
  );
}

export default CommunityGeneralList;
