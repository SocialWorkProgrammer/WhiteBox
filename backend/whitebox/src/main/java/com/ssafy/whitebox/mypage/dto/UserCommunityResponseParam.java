package com.ssafy.whitebox.mypage.dto;
import com.ssafy.whitebox.community.dto.CommunityCommentParam;

import lombok.Getter;
import lombok.Setter;


import java.util.List;
import java.time.LocalDateTime;
import com.ssafy.whitebox.user.entity.User;

@Getter
@Setter
public class UserCommunityResponseParam {
    private Long comIndex;
    private String comTitle;
    private LocalDateTime comCreatedAt;
    private int commentCount;
}