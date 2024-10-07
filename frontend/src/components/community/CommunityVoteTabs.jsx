import communityIcon from '../../public/img/community-general-deactive.svg'
import voteIcon from '../../public/img/community-vote.svg'
import "../../styles/community/communitygenrallist.css"

function CommunityGeneralTabs() {
  return (
    // 전체 컴포넌트
    <div className="grid grid-cols-12">
      {/* 그리드 좌측 여백 세 칸 차지 */}
      <div className="col-span-2"></div>
      {/* 여기부터 투표게시판 컴포넌트 */}
        <div className="max-w-[1300px] col-span-8 border-x-2 p-3">
          {/* 게시판 탭 */}
          <div className="flex flex-row">
            <a className="community-tab-active flex flex-row text-[25px] font-medium" href="/community/vote">
            <img 
                src={voteIcon}
                alt="자유"
                className="w-10 h-10"
                />
              투표
              </a>
            <a className="community-tab-deactive flex flex-row text-[25px] font-medium" href="/community/general">
            <img 
              src={communityIcon}
              alt="" 
              className="w-10 h-10"
              />
            <p>일반</p>
            </a>
            </div>
          {/* 게시판 안내 */}
          <div className="community-notice border-y-[0.5px] border-marvel-blue flex flex-col place-content-center p-1">
            <h1 className="text-3xl mb-4 font-semibold">투표 게시판</h1>
            <p className="text-xl">정치, 혐오글, 욕설 금지입니다.</p>  
          </div>
          </div>
          </div>
)}

export default CommunityGeneralTabs;
