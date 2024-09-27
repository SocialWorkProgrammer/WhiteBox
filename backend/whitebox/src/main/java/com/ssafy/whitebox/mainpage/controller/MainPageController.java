package com.ssafy.whitebox.mainpage.controller;

import com.ssafy.whitebox.mainpage.dto.MainPageVoteResponseParam;
import com.ssafy.whitebox.mainpage.service.MainPageService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/mainpage")
@RequiredArgsConstructor
public class MainPageController {

    private final MainPageService mainPageService;

    @GetMapping("/top-votes")
    public ResponseEntity<List<MainPageVoteResponseParam>> getTopVotes() {
        List<MainPageVoteResponseParam> topVotes = mainPageService.getTop6Votes();
        return ResponseEntity.ok(topVotes);
    }
}
