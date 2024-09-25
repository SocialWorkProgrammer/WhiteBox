package com.ssafy.whitebox.vote.dto;

import com.ssafy.whitebox.ai.entity.AIResult;
import com.ssafy.whitebox.vote.entity.Vote;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Setter
public class VoteDetailResponseParam {
    private Long voteId;
    private String title;
    private String description;
    private int approvalPercent;
    private int oppositePercent;
    private int neutralPercent;
    private LocalDateTime createdAt;
    private int hit;
    private boolean isImage;

    // AIResult 정보
    private String aiRelatedInformation;
    private String aiRelatedLaw;
    private int aiUserFault;
    private int aiOtherFault;
    private String videoUrl;

    // 이미지 리스트
    private List<VoteImageParam> images;

    // 댓글 리스트
    private List<VoteCommentParam> comments;
    public VoteDetailResponseParam(){

    }
    // 생성자
    public VoteDetailResponseParam(Vote vote, AIResult aiResult, List<VoteImageParam> images, List<VoteCommentParam> comments) {
        this.voteId = vote.getVoteId();
        this.title = vote.getVoTitle();
        this.description = vote.getVoDescription();
        this.approvalPercent = vote.getVoApprovalCnt();
        this.oppositePercent = vote.getVoOppositeCnt();
        this.neutralPercent = vote.getVoNeutralCnt();
        this.createdAt = vote.getVoCreatedAt();
        this.hit = vote.getVoHit();
        this.isImage = vote.isVoIsImage();

        // AIResult 정보
        this.aiRelatedInformation = aiResult.getAiRelatedInformation();
        this.aiRelatedLaw = aiResult.getAiRelatedLaw();
        this.aiUserFault = aiResult.getAiUserFault();
        this.aiOtherFault = aiResult.getAiOtherFault();
        this.videoUrl = aiResult.getVideoUrl();

        // 이미지 및 댓글 리스트
        this.images = images;
        this.comments = comments;
    }
}
