package com.ssafy.whitebox.community.dto;

import lombok.Setter;
import lombok.Getter;

@Getter
@Setter
public class CommentCreateParam {
    private Long userId;
    private String comment;

    // Getters and Setters
}