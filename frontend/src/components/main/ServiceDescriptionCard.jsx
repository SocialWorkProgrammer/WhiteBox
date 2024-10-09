import React from "react";
import sampleImg from "../../public/img/sample.jpg"
<<<<<<< HEAD

function ServiceDescriptionCard () {
    const data = [
        {title:'AI로 과실 측정', summary:'영상을 올리고, AI를 기다려요', description:'과실비율, 관련 법령, 판례 제공해줌', img:sampleImg},
        {title:'투표게시판', summary:'투표를 올리고, 사람들을 기다려요', description:'열띤 토론의 장을 펼쳐라', img:sampleImg},
        {title:'정보게시판', summary:'원하는 정보를 찾아봐요', description:'법령, 판례, 다 나와', img:sampleImg},
=======
import aiIcon from "../../public/img/ai-icon.svg"
import peopleIcon from "../../public/img/people-icon.svg"
import infoIcon from "../../public/img/info-icon.svg"

function ServiceDescriptionCard () {
    const data = [
        {title:'영상만 올리면, AI가 다 해줘요', summary:'AI로 과실 측정', description:'과실비율, 관련 법령, 판례 모두 제공해줘요', icon:aiIcon, img:sampleImg},
        {title:'투표 시스템을 통한 집단지성', summary:'집단지성의 활용', description:'변호사를 비롯한 사람들의 도움을 받을 수 있어요', icon:peopleIcon, img:sampleImg},
        {title:'교통 법령, 조례 찾기 힘들었죠?', summary:'교통정보를 한 눈에', description:'White-Box에서 한 번에 찾으세요', icon:infoIcon, img:sampleImg},
>>>>>>> FE-Develop

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
<<<<<<< HEAD
                    className={`flex ${index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'} bg-white rounded-lg shadow-md overflow-hidden mb-6`}
                    >
                        {renderImage(item.img)}
                        {renderText(item.title, item.summary, item.description)}
=======
                    className={`flex ${index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'} bg-gray-50 rounded-lg overflow-hidden mb-20 place-content-between`}
                    >
                        <img src={item.img} className="w-[400px] mx-10" />
                        <div className="flex flex-col mx-10">
                            <div className="flex flex-row gap-3 items-center mt-10">
                                <img src={item.icon} alt="" className="h-10 w-10"/>
                                <p className="text-center font-bold text-[#458EF7]">{item.summary}</p>
                            </div>
                            <div className="mt-5">
                                <h1 className="text-3xl font-bold">{item.title}</h1>
                                <p className="text-lg mt-20">{item.description}</p>
                            </div>
                        </div>
>>>>>>> FE-Develop
                    </div>
                ))}
            </div>
            <div className="col-span-2"></div>
        </div>
    )
}

export default ServiceDescriptionCard;