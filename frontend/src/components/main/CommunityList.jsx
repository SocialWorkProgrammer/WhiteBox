import React, { useEffect, useState } from "react";
import { useCommunityStore } from "../../store/useCommunityStore";
import { formatDistanceToNow, parseISO, differenceInDays, differenceInHours, differenceInMinutes } from "date-fns";
import { ko } from "date-fns/locale";
import { useNavigate } from "react-router-dom";
import useStore from "../../store/useStore";

function CommunityList({ type }) {
    const navigate = useNavigate();
    // 상위 3개 항목 배경 색 지정
    const highlightPosting = {
        0:"bg-indigo-300",
        1:"bg-indigo-200",
        2:"bg-indigo-100",
    }


    // 시간 포매팅 - 일반 게시판
    const formatingTime = (dateString) => {
        return formatDistanceToNow(parseISO(dateString), { addSuffix: true, locale: ko });
    }

    // 시간 포매팅 - 투표 게시판
    const formatingExpirationTime = (dateString) => {
        const now = new Date();
        const expiration = new Date(dateString)

        const daysLeft = differenceInDays(dateString, now);
        const hoursLeft = differenceInHours(dateString, now);
        const minutesLeft = differenceInMinutes(dateString, now);

        if (daysLeft > 1) {
            return `투표 만료까지 ${daysLeft}일 남음`;
        } else if (hoursLeft > 1) {
            return `투표 만료까지 ${hoursLeft}시간 남음`;
        } else if (minutesLeft > 0) {
            return `투표 만료까지 ${minutesLeft}분 남음`;
        } else {
            return "투표가 만료되었습니다";
        }
    }


    // 투표게시판인 경우
    const getVoteCommunityList = useCommunityStore(state => state.getMainVoteCommunityList)
    const [ voteCommunityList, setVoteCommunityList ] = useState([]);
    useEffect(() => {
        if (type === "vote") {
            const getData = async () => {
                try {
                    const response = await getVoteCommunityList({ pageIndex: 1 });
                    setVoteCommunityList(response || []);
                } catch (err) {
                    console.log(err);
                    setVoteCommunityList([]);
                } 
            }
            getData();
        }
    }, [type, getVoteCommunityList])

    // 투표게시판 렌더링
    const renderVoteCommunity = () => {
        return (
            <div className="flex-row">
                <div>
                    <span className="flex justify-center">투표 게시판</span>
                </div>
                {voteCommunityList?.map((item, index) => (
                    <div key={index} className={`grid grid-cols-4 border shadow m-2 cursor-pointer p-1 ${index < 3 ? highlightPosting[index] : ''}`} onClick={() => handleCommunityDetailClick({type:'vote', item})}>
                        <img src={item.thumbnail1} alt="" />
                        <span className="col-span-2 text-base truncate">{item.title}</span>
                        <div className="col-span-2">
                            <span className="text-xs truncate">투표 수 : {item.totalVotes}</span>
                            <br />
                            <span className="text-xs truncate">{formatingExpirationTime(item.expirationDate)}</span>
                        </div>
                        
                        
                    </div>
                ))}
                <div className="flex justify-end me-1" onClick={() => handleCommunityListClick('vote')} >
                    <span className="cursor-pointer text-xs">더보기</span>
                </div>
            </div>
        )
    }

    // 일반게시판
    const getGeneralCommunityList = useCommunityStore(state => state.getCommunityGeneralList)
    const [ generalCommunityList, setGeneralCommunityList ] = useState([]);
    useEffect(() => {
        if (type === "general") {
            const getData = async () => {
                try {
                    const response = await getGeneralCommunityList({ pageId:1 });
                    setGeneralCommunityList(response.content || []);
                } catch (err) {
                    console.log(err);
                    setGeneralCommunityList([]);
                } 
            }
            getData();
        }
    }, [type, getGeneralCommunityList])

    // 일반게시판 렌더링
    const renderGeneralCommunity = () => {
        return (
            <div className="flex-row ms-2">
                <div>
                    <span className="flex justify-center">일반 게시판</span>
                </div>
                {generalCommunityList?.map((item, index) => (
                    <div key={index} className={`grid grid-cols-4 border shadow m-2 cursor-pointer p-1 ${index < 3 ? highlightPosting[index] : ''}`} onClick={() => handleCommunityDetailClick({type:'general', item})}>
                        <span className="col-span-2 text-base truncate">{item.comTitle}</span>
                    <div className="col-span-1">
                        <span className="text-xs truncate">조회수 : {item.comHit}</span>
                    </div>
                    <div className="col-span-1">
                        <span className="text-xs truncate">{formatingTime(item.comCreatedAt)}</span>
                    </div>
                    </div>
                ))}
                <div className="flex justify-end me-1" onClick={() => handleCommunityListClick('general')} >
                    <span className="cursor-pointer text-xs">더보기</span>
                </div>
            </div>
        )
    }

    // 디테일페이지로 이동
    const handleCommunityDetailClick = ({type, item}) => {
        if (type === "general") {
            navigate(`/community/general/${item.comIndex}`)
        } else if (type === "vote") {
            navigate(`/community/vote/${item.voteId}`)
        }
    }

    // 더보기 클릭
    const handleCommunityListClick = (type) => {
        navigate(`/community/${type}`)
    }
    
    return (
        <div>
            {type === "vote" && renderVoteCommunity()}
            {type === "general" && renderGeneralCommunity()}
        </div>
    )
}

export default CommunityList