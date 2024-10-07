import React, { useEffect, useState } from 'react';
import "../../styles/auth/lawyer-auth-modal.css";
import useAuthStore from '../../store/useAuthStore';

function LawyerAuthModal({ closeModal }) {
    const authLawyer = useAuthStore((state) => state.authLawyer);
    const [ name, setName ] = useState('');
    const [ birth, setBirth ] = useState('');
    const [ file, setFile ] = useState(null);
    const [ isLoading, setIsLoading ] = useState(false);
    
    const handleFileChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);
        } else {
            setFile(null);
        }
    }

    const handleSubmit = async () => {
        setIsLoading(true);
        if (name === '') {
            window.alert('이름을 입력하세요');
            setIsLoading(false);
            return;
        } else if (birth === '') {
            window.alert('생일을 입력하세요');
            setIsLoading(false);
            return;
        } else if (file === null) {
            window.alert('파일을 업로드하세요');
            setIsLoading(false);
            return;
        } else {
            const response = await authLawyer({ name, date: birth, image: file })
            if (response.message === "변호사 인증 성공!") {
                localStorage.setItem('isLawyer', 'true');
                window.alert('인증 성공하였습니다.');
                setIsLoading(false);
                closeModal();
                return;
            } else {
                window.alert('인증 실패하였습니다.');
                setIsLoading(false);
                closeModal();
                return;
            }
        }
    }

    return (
        <div>
            {/* 이름 받기 */}
            <div className="mb-4 flex items-center">
                <label className="block text-gray-700 w-1/4">이름</label>
                <input
                    type="text"
                    className="w-3/4 px-3 py-2 border rounded-lg"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </div>
            {/* 생일 받기 */}
            <div className="mb-4 flex items-center">
                <label className="block text-gray-700 w-1/4">생일</label>
                <input 
                    type="date"
                    className="w-3/4 px-3 py-2 border rounded-lg"
                    value={birth}
                    onChange={(e) => setBirth(e.target.value)}
                    max={new Date().toISOString().split("T")[0]}
                />
            </div>
            {/* 파일 받기 */}
            <div className="mb-4 flex items-center">
                <label className="block text-gray-700 w-1/4">이미지 업로드</label>
                <input
                    type="file"
                    accept="image/*"
                    className="w-3/4"
                    onChange={handleFileChange}
                />
            </div>
            {/* 제출 하기 */}
            <div className='flex justify-between'>
                <button
                    onClick={closeModal}
                    className="px-4 py-2 rounded-lg hover:bg-gray-300"
                    disabled={isLoading}
                    >
                    취소
                </button>
                <button
                    onClick={() => handleSubmit()}
                    className={`px-4 py-2 rounded-lg hover:bg-gray-300 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    disabled={isLoading}
                >
                    제출
                </button>
            </div>
        </div>
    );
}

export default LawyerAuthModal;