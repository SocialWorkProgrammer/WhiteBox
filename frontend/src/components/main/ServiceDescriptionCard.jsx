import React from "react";
import sampleImg from "../../public/img/sample.jpg"
import aiIcon from "../../public/img/ai-icon.svg"
import peopleIcon from "../../public/img/people-icon.svg"
import infoIcon from "../../public/img/info-icon.svg"
import infoMain from '../../public/img/info-main.png'
import voteMain from '../../public/img/vote-main.png'

function ServiceDescriptionCard () {
    const data = [
        {title:'영상만 올리면, AI가 다 해줘요', summary:'AI로 과실 측정', description:'과실비율, 관련 법령, 판례 모두 제공해줘요', icon:aiIcon, img:sampleImg},
        {title:'투표 통한 의견나눔', summary:'집단지성의 활용', description:'변호사를 비롯한 사람들의 도움을 받을 수 있어요', icon:peopleIcon, img:voteMain},
        {title:'교통 법률 찾기 힘들었죠?', summary:'교통정보를 한 눈에', description:'White-Box에서 한 번에 찾으세요', icon:infoIcon, img:infoMain},

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
                    className={`flex ${index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'} bg-gray-50 rounded-lg overflow-hidden mb-20 place-content-between`}
                    >
                        <img src={item.img} className="w-[500px] mx-10" />
                        <div className="relative flex flex-col mx-10">
                            <div className="flex flex-row gap-3 items-center mt-10">
                                <img src={item.icon} alt="" className="h-10 w-10"/>
                                <p className="text-center font-bold text-[#458EF7]">{item.summary}</p>
                            </div>
                            <div className="mt-5">
                                <h1 className="text-3xl font-bold">{item.title}</h1>
                                <p className="text-lg mt-20">{item.description}</p>
                            </div>
                                <div className="absolute bottom-0">
                                    <p className="text-sm text-red-500 text-[10px]">※ 회원가입 시 모두 이용 가능합니다.</p>
                                    <a href="/auth/sign-up" className="text-sm underline underline-offset-2 text-blue-500">회원가입 링크</a>
                                </div>
                        </div>
                    </div>
                ))}
            </div>
            <div className="col-span-2"></div>
        </div>
    )
}

export default ServiceDescriptionCard;