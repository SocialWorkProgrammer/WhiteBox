import React, { useEffect, useState } from 'react';
import useStore from '../../store/useStore';
import axios from 'axios';

const BASE_URL = useStore.getState().BASE_URL;

const ImageSlider = ({ thumbnail1, thumbnail2, thumbnail3, thumbnail4, className }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [images, setImages] = useState([]);

    useEffect(() => {
        const loadImages = () => {
            setImages([
                thumbnail1,
                thumbnail2,
                thumbnail3,
                thumbnail4,
               
            ]);
        };

        loadImages();
        
        // setInterval을 통해 인덱스를 변경
        const intervalId = setInterval(() => {
            setCurrentIndex((prevIndex) => (prevIndex + 1) % 4); // 4는 이미지 수
        }, 2000); // 2초마다 이미지 변경

        return () => clearInterval(intervalId);
    }, [thumbnail1, thumbnail2, thumbnail3, thumbnail4]);

    return (
        <div>
            <img src={`/thumbnails/b8a827a6-4e0c-4d52-a0ca-6a43e2d47192.jpg`} alt={`Slide ${currentIndex}`} className={`${className}`}/>
        </div>
    );
};

export default ImageSlider;
