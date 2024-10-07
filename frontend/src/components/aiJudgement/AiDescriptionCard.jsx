import React from "react";

function AiDescriptionCard ({ type, content }) {
    let title;
    switch (type) {
        case 'ratio':
            title = '과실 비율'
            break;
        case 'situation':
            title = '사고 상황'
            break;
        case 'description':
            title = '과실 비율 해설'
            break;
        case 'law':
            title = '관련 법규'
            break;
        case 'precedent':
            title = '관련 판례 및 사례'
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