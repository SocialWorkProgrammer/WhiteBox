package com.ssafy.whitebox.vote.dto;

import java.util.List;
import lombok.Getter;

@Getter
public class VoteCreateRequestParam {
    private String title;
    private String description;

    private List<String> images;


}
