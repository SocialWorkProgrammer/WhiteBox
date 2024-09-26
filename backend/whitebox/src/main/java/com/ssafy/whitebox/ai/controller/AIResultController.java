package com.ssafy.whitebox.ai.controller;

import com.ssafy.whitebox.ai.entity.AIResult;
import com.ssafy.whitebox.ai.service.AIResultService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
public class AIResultController {

    private final AIResultService aiResultService;

    @PostMapping("/upload-video")
    public ResponseEntity<AIResult> uploadVideo(@AuthenticationPrincipal UserDetails userDetails,
                                                @RequestPart("video") MultipartFile videoFile) throws IOException, InterruptedException {
        AIResult aiResult = aiResultService.createAIResult(userDetails.getUsername(), videoFile);
        return ResponseEntity.ok(aiResult);
    }

//    @GetMapping
//    public ResponseEntity<List<AIResult>> getAllAIResults() {
//        List<AIResult> aiResults = aiResultService.getAllAIResults();
//        return ResponseEntity.ok(aiResults);
//    }
//
//    @GetMapping("/{id}")
//    public ResponseEntity<AIResult> getAIResultById(@PathVariable Long id) {
//        AIResult aiResult = aiResultService.getAIResultById(id);
//        return ResponseEntity.ok(aiResult);
//    }
}
