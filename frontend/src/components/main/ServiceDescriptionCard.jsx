import React from "react";
import sampleImg from "../../public/img/sample.jpg"

function ServiceDescriptionCard () {
    const data = [
        {title:'AI로 과실 측정', summary:'영상을 올리고, AI를 기다려요', description:'과실비율, 관련 법령, 판례 제공해줌', img:sampleImg},
        {title:'투표게시판', summary:'투표를 올리고, 사람들을 기다려요', description:'열띤 토론의 장을 펼쳐라', img:sampleImg},
        {title:'정보게시판', summary:'원하는 정보를 찾아봐요', description:'법령, 판례, 다 나와', img:sampleImg},

    ]
    const renderImage = (img) => {
        return (
            <div className="w-1/2 p-4">
                <img 
                    src={img} 
                    alt="" 
                    className="rounded-lg shadow-lg w-full h-auto object-cover" 
                />
            </div>
        );
    };

    const renderText = (title, summary, description) => {
        return (
            <div className="w-1/2 pt-40 ps-20">
                <h2 className="text-3xl font-bold mb-2">{title}</h2>
                <p className="text-xl text-gray-700 font-semibold mb-2">{summary}</p>
                <p className=" text-gray-500">{description}</p>
            </div>
        );
    };
    return (
        <div className="container mx-auto grid grid-cols-12">
            <div className="col-span-2"></div>
            <div className="col-span-8">
                {data.map((item, index) => (
                    <div 
                    key={index} 
                    className={`flex ${index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'} bg-white rounded-lg shadow-md overflow-hidden mb-6`}
                    >
                        {renderImage(item.img)}
                        {renderText(item.title, item.summary, item.description)}
                    </div>
                ))}
            </div>
            <div className="col-span-2"></div>
        </div>
    )
}

export default ServiceDescriptionCard;