package com.ssafy.whitebox.ai.controller;

import com.ssafy.whitebox.ai.entity.Lawyer;
import com.ssafy.whitebox.ai.service.LawyerService;
import com.ssafy.whitebox.user.entity.User;
import com.ssafy.whitebox.user.service.UserService;
import com.ssafy.whitebox.user.util.UserType;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.Date;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/v1/")
public class LawyerController {

    private final LawyerService lawyerService;
    private final UserService userService;

    @PostMapping("/verify-lawyer")
    public ResponseEntity<String> verifyLawyer(
            @RequestParam String name,
            @RequestParam Date date,
            @RequestParam String email,
            @RequestParam MultipartFile file) {

        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String currentUserEmail = (String) authentication.getPrincipal();

        Lawyer lawyer = lawyerService.findLawyerByNameAndDate(name, date);
        if (lawyer == null) {
            return ResponseEntity.status(404).body("변호사를 찾을 수 없습니다.");
        }

        // Python 서버로 이미지 검증 요청
        ResponseEntity<String> response = lawyerService.verifyLawyerImageWithPython(name, date, email, file, lawyer.getLawyerImageUrl());

        if (response.getStatusCode().is2xxSuccessful() && response.getBody().contains("변호사 인증 성공!")) {
            User user = userService.getUserByEmail(email);

            user.userType(UserType.LAWYER);
            userService.saveUser(user);

            return ResponseEntity.ok("변호사 인증 및 상태 업데이트 완료");
        } else {
            return ResponseEntity.ok("변호사 인증 실패");
        }
    }
}
