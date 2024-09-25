package com.ssafy.whitebox.mypage.controller;

import com.ssafy.whitebox.mypage.dto.UserInfoResponseParam;
import com.ssafy.whitebox.mypage.service.MyPageService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/my")
@RequiredArgsConstructor
public class MyPageController {

    private final MyPageService myPageService;

    @GetMapping
    public ResponseEntity<UserInfoResponseParam> getUserInfo(@AuthenticationPrincipal UserDetails userDetails) {
        UserInfoResponseParam userInfo = myPageService.getUserInfo(userDetails);
        return ResponseEntity.ok(userInfo);
    }
}
