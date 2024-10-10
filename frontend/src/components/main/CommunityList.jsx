import React, { useEffect, useState } from "react";
import { useCommunityStore } from "../../store/useCommunityStore";
import { formatDistanceToNow, parseISO, differenceInDays, differenceInHours, differenceInMinutes } from "date-fns";
import { ko } from "date-fns/locale";
import { useNavigate } from "react-router-dom";
import { Tooltip } from "react-tooltip";

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

    // 게시판 목록 로드
    const [ voteCommunityList, setVoteCommunityList ] = useState([]);
    const [ generalCommunityList, setGeneralCommunityList ] = useState([]);
    const getCommunityList = useCommunityStore((state) => state.getMainCommunityList)

    useEffect(() => {
        const getData = async () => {
            try {
                const response = await getCommunityList();
                setVoteCommunityList(response.votes || []);
                setGeneralCommunityList(response.communities || []);
            } catch (err) {
                console.log(err);
            }
        }
        getData();
    }, [])


    // 투표게시판 렌더링
    const renderVoteCommunity = () => {
        return (
            <div className="flex-row">
                <div className="flex justify-center">
                    <span 
                        id="vote-list-title-tooltip"
                        className="cursor-pointer" 
                        onClick={() => handleCommunityListClick('vote')}
                        data-tooltip-id="vote-list-title-tooltip"
                        data-tooltip-content="투표게시판으로 이동"
                    >
                        투표 게시판
                    </span>
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
                {(voteCommunityList.length === 0) && (
                    <div className="m-2 p-1 text-sm">게시글이 없습니다.</div>
                )}
                <Tooltip id="vote-list-title-tooltip" place="right"/>
            </div>
        )
    }

    // 일반게시판 렌더링
    const renderGeneralCommunity = () => {
        return (
            <div className="flex-row ms-2">
                <div className="flex justify-center">
                    <span 
                        id="general-list-title-tooltip"
                        className="cursor-pointer" 
                        onClick={() => handleCommunityListClick('general')}
                        data-tooltip-id="general-list-title-tooltip"
                        data-tooltip-content="일반게시판으로 이동"
                    >
                        일반 게시판
                    </span>
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
                {(generalCommunityList.length === 0) && (
                    <div className="m-2 p-1 text-sm">게시글이 없습니다.</div>
                )}
                <Tooltip id="general-list-title-tooltip" place="right"/>
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