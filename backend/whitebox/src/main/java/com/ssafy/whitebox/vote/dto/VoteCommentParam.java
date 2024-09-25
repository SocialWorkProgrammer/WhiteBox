package com.ssafy.whitebox.vote.dto;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
public class VoteCommentParam {
    private String userNickname;
    private String comment;
    private LocalDateTime postedAt;

    public VoteCommentParam(String userNickname, String comment, LocalDateTime postedAt) {
        this.userNickname = userNickname;
        this.comment = comment;
        this.postedAt = postedAt;
    }
}
