import React, { useEffect, useState } from "react";
import useAuthStore from "../../store/useAuthStore";
import { useNavigate } from "react-router-dom";

function MyVoteList () {
    const navigate = useNavigate();
    const [ voteList, setVoteList ] = useState([]);
    const [ pageId, setPageId ] = useState(1);
    const [ totalVoteCount, setTotalVoteCount ] = useState(0);
    const loadVoteList = useAuthStore((state) => state.getMyVotes);
    const itemsPerPage = 6;

    useEffect(() => {
        const fetchVoteList = async () => {
            const fetchedVoteList = await loadVoteList({ pageId });
            console.log(fetchedVoteList);
            setVoteList(fetchedVoteList.userVotes);
            setTotalVoteCount(fetchedVoteList.totalVotes)
        }
        fetchVoteList();
    }, [pageId, loadVoteList]);

    const totalPages = Math.ceil(totalVoteCount / itemsPerPage);

    const handlePageChange = (newPageId) => {
        if (pageId >= 1 && newPageId <= totalPages) {
            setPageId(newPageId);
        }
    }

    const handleClickDetail = ({voteId}) => {
        navigate(`/community/vote/${voteId}`);
    }

    return (
        <div className="mt-3">
            {/* 투표목록 */}
            {voteList.map((vote) => (
                <div key={vote.voteId} onClick={() => handleClickDetail({voteId:vote.voteId})} className="border shadow m-2">
                    <span>글 제목 : {vote.title}</span>
                    <span>투표비율 : {vote.approvalPercent} : {vote.neutralPercent} : {vote.oppositePercent}</span>
                    <span>투표수 : {vote.voteCount}</span>
                    <span>댓글 수 : {vote.commentCount}</span>
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

export default MyVoteList;


