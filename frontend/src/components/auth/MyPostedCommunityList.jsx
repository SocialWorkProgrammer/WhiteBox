import React, { useEffect, useState } from "react";
import useAuthStore from "../../store/useAuthStore";
import { useNavigate } from "react-router-dom";
import { formatDistanceToNow, parseISO } from "date-fns";
import { ko } from "date-fns/locale";

function MyPostedCommunityList () {
    const navigate = useNavigate();
    const loadMyPostings = useAuthStore((State) => State.getMyPostings);
    const [ myPostings, setMyPostings ] = useState([]);
    const [ pageId, setPageId ] = useState(1);
    const [ postsCount, setPostsCount ] = useState(0);
    const itemsPerPage = 3;

    // 시간 포매팅
    const formattingTime = (dateString) => {
        return formatDistanceToNow(parseISO(dateString), { addSuffix: true, locale: ko });
    }

    useEffect(() => {
        const fetchMyPosts = async() => {
            const fetchedMyPosts = await loadMyPostings({ pageId })
            console.log(fetchedMyPosts);
            setMyPostings(fetchedMyPosts.userCommunities);
            setPostsCount(fetchedMyPosts.totalCommunities);
        };
        fetchMyPosts();
    }, [pageId, loadMyPostings])

    const totalPages = Math.ceil(postsCount / itemsPerPage);
    const handlePageChange = (newPageId) => {
        if (newPageId >= 1 && newPageId <= totalPages) {
            setPageId(newPageId);
        }
    }

    const handleClickDetail = ({ pageId }) => {
        navigate(`/community/general/${pageId}`)
    }

    return (
        <div className="mt-3">
            {/* 영상 목록 */}
            {myPostings.map((post) => (
                <div key={post.comIndex} className="grid grid-cols-12 border shadow m-2">
                    <span className="col-span-8 cursor-pointer" onClick={() => handleClickDetail({pageId:post.comIndex})}>{post.comTitle}</span>
                    <div className="col-span-4">
                        <span className="text-sm">{formattingTime(post.comCreatedAt)}</span>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        <span className="text-sm">조회수 : {post.commentCount}</span>
                    </div>
                </div>  
            ))}
            {/* 페이지네이션 */}
            <div className="mt-3 flex justify-center items-center">
                <span className="me-2 cursor-pointer" onClick={() => handlePageChange(1)}>&lt;&lt;</span>
                <span className="me-2 cursor-pointer" onClick={() => handlePageChange(pageId - 1)}>&lt;</span>
                {Array.from({ length: totalPages }, (_, index) => (
                    <button
                        key={index}
                        onClick={() => handlePageChange(index + 1)}
                        className={`cursor-pointer p-2 ${pageId === index + 1? "bg-gray-400 text-white" : "hover:bg-gray-300"}`}
                    >
                        {index + 1}
                    </button>
                ))}
                <span className="me-2 cursor-pointer" onClick={() => handlePageChange(pageId + 1)}>&gt;</span>
                <span className="me-2 cursor-pointer" onClick={() => handlePageChange(totalPages)}>&gt;&gt;</span>
            </div>
        </div>
    )
}

export default MyPostedCommunityList;