import React from "react";
import { useNavigate } from "react-router-dom";

function WriteButton({ route, className="", name }) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(route);
  };
  return (
    <button
      className={`border-2 w-[95px] h-[38px] ${className}`}
      onClick={handleClick}>
        {name}
      </button>
  )
}

export default WriteButton;