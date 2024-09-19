package com.ssafy.whitebox.community.dto;
import lombok.Getter;
import lombok.Setter;


import java.util.List;
import java.time.LocalDateTime;
//import com.ssafy.whitebox.user.dto.UserParam;
import com.ssafy.whitebox.user.entity.User;

@Getter
@Setter
public class CommunityParam {
    private Long comIndex;
    private String comTitle;
    private String comDescription;
    private LocalDateTime comCreatedAt;
    private int comHit;
    private boolean comIsImage;
    private List<CommunityImageParam> images;
    private Long userIndex;
    private String userNickname;
    private User user;
    private List<CommunityCommentParam> comments;
}


