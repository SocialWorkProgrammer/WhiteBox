import React from "react";
import { useNavigate } from 'react-router-dom';
import { useCommunityStore } from "../../store/useCommunityStore";
import useStore from "../../store/useStore";

function SubmitButton({ title, description, className, images }) {
  const BASE_URL = useStore.getState().BASE_URL;
  const postCommunityGeneral = useCommunityStore((state) => state.postCommunityGeneral);
  const navigate = useNavigate();
  console.log(images)
  // Base64 문자열을 Blob으로 변환하는 함수
  const base64ToBlob = (base64Data) => {
    const byteCharacters = atob(base64Data.replace(/^data:image\/jpeg;base64,/, ""));
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    return new Blob([new Uint8Array(byteNumbers)], { type: 'image/jpeg' });
  };

  // onSubmit 함수
  const onSubmit = async () => {
    try {
      console.log('제목:', title, '내용:', description, '이미지들:', images);
      if (title === '') {
        alert('제목을 입력하세요');
        return; // 입력 체크 후 함수 종료
      }
      else if (description === '') {
        alert('내용을 입력하세요');
        return; // 입력 체크 후 함수 종료
      }

      // Base64 이미지 배열을 Blob으로 변환
      const imageBlobs = images.map(base64ToBlob);
      console.log(imageBlobs);
      // postCommunityGeneral 호출 시 Blob 배열 전달
      const response = await postCommunityGeneral({ title, description, images: imageBlobs });
      console.log('등록된 게시글', response);
      navigate(`../general/${response.data.comIndex}`);
    } catch (err) {
      console.log('submit버튼에 뜬 에러', err);
    }
  };

  return (
    <button
      className={`border-2 w-[95px] h-[38px] ${className}`}
      onClick={onSubmit}>
      제출
    </button>
  );
}

export default SubmitButton;
