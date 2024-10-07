import React, { useState } from 'react'; 
import ServiceDescriptionCard from './ServiceDescriptionCard';
import CommunityList from './CommunityList';
import { useNavigate } from 'react-router-dom';
import ClipLoader from 'react-spinners/ClipLoader';
import useAIStore from '../../store/useAIStore.jsx'
import { Helmet } from 'react-helmet';

function Main() {
    const navigate = useNavigate();
    // isLogin 받기
    const isLogin = localStorage.getItem('accessToken');
    // 로딩중
    const [ isLoading, setIsLoading ] = useState(false);
    // 비디오파일
    const [ videoFile, setVideoFile ] = useState(null);
    const [ videoName, setVideoName ] = useState(null);
    const getAiJudgement = useAIStore((state) => state.getAiJudgement)
    const uploadVideo = useAIStore((state) => state.uploadVideo);
    // 파일 드래그 앤 드롭
    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('video/')) {
            setVideoFile(file);
            setVideoName(file.name);
        }
    }
    const handleDragOver = (e) => {
        e.preventDefault();
    }
    // 파일 첨부
    const handleFileInputChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith('video/')) {
            setVideoFile(file);
            setVideoName(file.name);
        }
    }

    // 파일 삭제
    const handleRemoveFile = () => {
        setVideoFile(null);
        setVideoName(null);
    }

    // ai 가랏
    const handleClickAiJudegement = async() => {
        if (!isLogin) {
            window.alert("Please login");
            navigate('/auth/login')
        } else {
            setIsLoading(true);
            // ai 판단 api 보내기, 판단 끝나면 ai-detail페이지로 이동하기
            const response = await uploadVideo({video:videoFile});
            console.log(response);
            navigate(`/ai-judgement/${response.data.id}`)
            setIsLoading(false)
            return;
        }
    }

    return (
        <div>
            <Helmet>
                <title>White Box</title>
            </Helmet>
            {isLoading ? (
                <div className="flex flex-col items-center justify-center h-full" style={{ height: 'calc(100vh - 90px)' }}>
                    <ClipLoader size={40} color={"#3498db"} loading={isLoading} />
                    <p className="mt-4">로딩 중...</p>
                    <p className="mt-4">약 1분 정도 소요됩니다.</p>
                </div>
            ) : (
                
                <div className="w-[100vw] grid grid-cols-12 gap-4 h-full" style={{ height: 'calc(100vh - 90px)' }}>
                    <div className="col-span-2"></div>
                    {/* gif 파일 */}
                    <div className="col-span-4 bg-gray-300 flex items-center justify-center">
                        <img src="" alt="GIF" className="max-w-full max-h-full" />
                    </div>
                    
                    {/* 비디오 드래그 앤 드롭 */}
                    <div 
                        className="col-span-4 bg-gray-200 flex items-center justify-center"
                        onDrop={ handleDrop }
                        onDragOver={ handleDragOver }
                    >
                        {videoFile ? (
                            <div>
                                <div>
                                    <span>{videoName}</span>
                                    <button onClick={handleRemoveFile} className='mt-2 bg-red-500 text-white px-4 py-2 rounded cursor-pointer'>
                                        x
                                    </button>
                                </div>
                                <div>
                                    <button onClick={handleClickAiJudegement} className='mt-2 bg-blue-500 text-white px-4 py-2 rounded cursor-pointer'>
                                        AI판단 보러 가기
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <div className="flex flex-col items-center space-y-4">
                                <p>드래그 앤 드롭 구역</p>
                                <input
                                    id="fileInput"
                                    type="file" 
                                    accept="video/*" 
                                    onChange={handleFileInputChange} 
                                    className="hidden"
                                />
                                <label 
                                    htmlFor="fileInput" 
                                    className="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer"
                                >
                                    파일 첨부
                                </label>
                            </div>
                            
                        )}
                    </div>
                    <div className="col-span-2"></div>
                </div>
            )}
            <div className="mt-3">
                {isLogin ? (
                    <div className='grid grid-cols-12'>
                        <div className='col-span-2'></div>
                        {/* 투표게시판 */}
                        <div className='col-span-4 m-1 w-full'>
                            <CommunityList type="vote"/>
                        </div>
                        {/* 일반게시판 */}
                        <div className='col-span-4 m-1 w-full'>
                            <CommunityList type="general"/>
                        </div>
                        <div className='col-span-2'></div>
                    </div> 
                    ) : (
                    <ServiceDescriptionCard />
                )}
            </div>
        </div>
    );
}

export default Main;
