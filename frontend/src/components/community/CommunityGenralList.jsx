import React, {useEffect, useState} from 'react';
import "../../styles/community/communitygenrallist.css"
// 다른 컴포넌트 가져오기
import Pagination from "./CommunityPagination";
import WriteButton from '../buttons/WriteButton';
import CommunityGeneralTabs from './CommunityGeneralTabs';
// Store 불러오기
import { useCommunityStore } from '../../store/useCommunityStore';
import { Helmet } from 'react-helmet';

function CommunityGeneralList() {
  const getCommunityGeneralList = useCommunityStore((state) => state.getCommunityGeneralList); // 게시판 목록 불러오기
  const [data, setData] = useState([]);
  const [totalElements, setTotalElements] = useState(); // 총 게시물 수
  const [currentPage, setCurrentPage] = useState(1); // 현재 페이지와, 이동할 페이지, default 값은 1
  const [itemsPerPage] = useState(10); // 한 페이지에 들어갈 아이템의 수
  const handlePageChange = (page) => {
    setCurrentPage(page);
  }
  
  useEffect(() => {
    const loadCommunityGeneralList = async () => {
        try {
          const responseData = await getCommunityGeneralList({ pageId:currentPage });
          // 여기서 setData(가공된 responseData)를 통해서 데이터설정을 해주세용
          setData(responseData.content)
          setTotalElements(responseData.totalElements)
          console.log('responseData.content==', responseData.content)
        } catch (err) {
          console.log(err);
        }
      }
      loadCommunityGeneralList();
    }, [currentPage]);
    
  // 페이지네이션 관련 변수들
  const indexOfLastItem = itemsPerPage; 
  const indexOfFirstItem = 0;
  const currentItems = data.length > 0 ? data.slice(indexOfFirstItem, Math.min(indexOfLastItem, indexOfFirstItem + data.length)): [];
  
  return (
    // 전체 컴포넌트
    <div>
      <Helmet>
        <title>White Box | 일반게시판</title>
      </Helmet>
      <CommunityGeneralTabs />
    <div className="grid grid-cols-12 border-b-2">
      {/* 그리드 좌측 여백 세 칸 차지 */}
      <div className="col-span-2"></div>
      {/* 여기부터 자유게시판 컴포넌트 */}
        <div className="max-w-[1300px] col-span-8 border-x-2 p-3">
          {/* 게시판 탭 */}
          {/* 게시판 */}
          <div className="flex flex-row text-[13px] place-content-between">
          <div className="flex flex-row">
            <div className="block w-[50px] text-center">번호</div>
            <div className="block ml-7">제목</div>
          </div>
          <div className="flex w-[300px] items-center place-content-between">
            <div className="w-[100px] text-center" >댓글수</div>
            <div className="w-[100px] text-center">조회수</div>
            <div className="w-[100px] text-center">작성자</div>
          </div>
          </div>
          <div className="mt-2 border-t-2">
          {currentItems.length > 0 ? (
            currentItems.map((item) => (
            <a href={`/community/general/${item.comIndex}`} className="flex flex-row  border-b-[0.5px] border-black h-[50px] text-xl place-content-between items-center" key={item.comIndex}>
              <div className="flex flex-row">
                <div className="w-[50px] text-center">{item.comIndex}</div>
                <div className="block font-light ml-7 max-w-[25vw] overflow-hidden text-ellipsis whitespace-nowrap" key={item.idx}>{item.comTitle}</div>
              </div>
              <div className="flex w-[300px] place-content-between">
                {item.commentCount ?
                  <div className="w-[100px] text-center font-light" key={item.idx}>[{item.commentCount}]</div>
                  : <div className="w-[100px] text-center">[0]</div>
                }
                <div className="w-[100px] text-center" key={item.comIndex}>{item.comHit}</div>
                <div className="w-[100px] font-bold text-center overflow-hidden text-ellipsis whitespace-nowrap" key={item.idx}>{item.userNickname}</div>
              </div>
            </a>
          ))): (
            <p>작성된 글이 없습니다.</p>
          )}
          </div>
          <div className="relative w-auto h-[38px] mt-5 mb-10">
          <WriteButton 
            route="/community/general/post"
            className="absolute right-0"
            name="작성하기" />
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
