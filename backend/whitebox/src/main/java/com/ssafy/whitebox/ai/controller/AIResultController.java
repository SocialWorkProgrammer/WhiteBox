package com.ssafy.whitebox.ai.controller;

import com.ssafy.whitebox.ai.entity.AIResult;
import com.ssafy.whitebox.ai.entity.Lawyer;
import com.ssafy.whitebox.ai.repository.LawyerRepository;
import com.ssafy.whitebox.ai.service.AIResultService;
import com.ssafy.whitebox.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.reactive.function.client.WebClient;

import java.io.IOException;
import java.util.Date;
import java.util.List;

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
public class AIResultController {

    private final WebClient webClient;
    private final UserRepository userRepository;
    private final LawyerRepository lawyerRepository;
    private final AIResultService aiResultService;

    @PostMapping("/upload-video")
    public ResponseEntity<AIResult> uploadVideo(@AuthenticationPrincipal UserDetails userDetails,
                                                @RequestPart("video") MultipartFile videoFile) throws IOException, InterruptedException {
        AIResult aiResult = aiResultService.createAIResult(userDetails.getUsername(), videoFile);
        return ResponseEntity.ok(aiResult);
    }


}
