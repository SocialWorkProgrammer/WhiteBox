import React from "react";

function AiDescriptionCard ({ type, content }) {
    let title;
    switch (type) {
        case 'ratio':
            title = '과실 비율'
            break;
        case 'situation':
<<<<<<< HEAD
            title = '사고 상황'
            break;
        case 'description':
            title = '과실 비율 해설'
=======
            title = '법적 기준 및 결론'
            break;
        case 'description':
            title = '사고 발생 상황 분석'
>>>>>>> FE-Develop
            break;
        case 'law':
            title = '관련 법규'
            break;
        case 'precedent':
<<<<<<< HEAD
            title = '관련 판례 및 사례'
=======
            title = '과실 비율 및 근거'
>>>>>>> FE-Develop
            break;
        default:
            title = '';
            break;
    }
    const renderCard = () => {
        return (
            <div className="mt-5">
                <span className="text-2xl font-semibold">{title}</span>
                <br />
                {type === 'ratio' ? <span className="ms-3">{content[0]} : {content[1]}</span>:<span className="ms-3">{content}</span>}
                <hr />
            </div>
        )
    }

    return renderCard();
}

export default AiDescriptionCard;