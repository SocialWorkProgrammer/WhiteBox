import React, { useEffect, useState } from "react";
import AiDescriptionCard from "./AiDescriptionCard";
import { useNavigate, useParams } from "react-router-dom";
import useAIStore from "../../store/useAIStore";
import AiVoteModal from "./AiVoteModal";

const initData = {
    aiCreatedAt:'"2024-09-27T17:09:52.709755"',
    aiOtherFault:50,
    aiUserFault:50,
    aiRelatedInformation:'',
    aiRelatedLaw:'',
    uploaded:false,
    voteIndex:1
}

function AiDetail () {
    const navigate = useNavigate();
    const { id } = useParams();
    const [ data, setData ] = useState(initData);
    const getData = useAIStore((state) => state.getAIResult)
    const [ videoSrc, setVideoSrc] = useState('');
    const [ showVoteModal, setShowVoteModal ] = useState(false);

    const handleAiVoteModal = () => {
        setShowVoteModal(true);
    }
    const closeAiVoteModal = () => {
        setShowVoteModal(false);
    }

    const navigateVoteDetail = () => {
        if (window.confirm("투표게시판으로 이동하시겠습니까?")) {
            navigate(`/community/vote/${data.voteIndex}`)
        }
    }

    useEffect(() => {
        const fetchData = async () => {
            const fetchedData = await getData({ id });
            setData(fetchedData);
            // setVideoSrc("https://whitebox-lawyer-vertify.s3.ap-northeast-2.amazonaws.com/videos/a2aa34e2-b366-4d60-8784-efa7238c10ad.mp4");
            setVideoSrc(fetchedData.aiVideoUrl);
            console.log(fetchedData);
        }
        fetchData();
    }, [getData, id])

    const formatData = (date) => {
        const newDate = new Date(date);
        const year = newDate.getFullYear();
        const month = String(newDate.getMonth() + 1).padStart(2, '0'); 
        const day = String(newDate.getDate()).padStart(2, '0');
        const hours = String(newDate.getHours()).padStart(2, '0');
        const minutes = String(newDate.getMinutes()).padStart(2, '0');
        const seconds = String(newDate.getSeconds()).padStart(2, '0');

        return `${year}년 ${month}월 ${day}일 ${hours}:${minutes}:${seconds}`;
    };

    return (
        <div className="mt-5">
            <div className="border border-gray-300 rounded-lg bg-black text-white">
                <video controls autoplay>
                    <source src={videoSrc} type="video/mp4" />
                </video>
            </div>
            <div className={`&${showVoteModal ? 'blur-xl' : ''}`}>
                <p>영상올린날짜 : {formatData(data.aiCreatedAt)}</p>
                <div className="grid grid-cols-2 gap-4">
                    <div className="col-span-1">
                        
                        <AiDescriptionCard type='ratio' content={[data.aiOtherFault, data.aiUserFault]}/>
                        <AiDescriptionCard type='precedent' content={data.aiExplanation}/>
                    </div>
                    <div className="col-span-1">
                        <AiDescriptionCard type='description'content={data.aiDescription}/>
                        <AiDescriptionCard type='situation' content={data.aiResult}/> 
                        <AiDescriptionCard type='law' content={data.aiRelatedLaw}/>
                    </div>
                </div>
                <div className="grid grid-cols-4 gap-4">
                    <div className="col-span-3"></div>
                    {data.uploaded ? 
                        <div onClick={navigateVoteDetail} className="cursor-pointer border rounded-lg p-2 text-center">투표게시판 이동</div>
                        : 
                        <div onClick={handleAiVoteModal} className="cursor-pointer border rounded-lg p-2 text-center">투표올리기</div>
                    }
                </div>
            </div>
            {showVoteModal && <AiVoteModal id={id} closeModal={closeAiVoteModal} videoSrc={videoSrc}/>}
        </div>
    )
}

export default AiDetail;