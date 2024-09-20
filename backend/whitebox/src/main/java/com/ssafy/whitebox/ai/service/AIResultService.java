package com.ssafy.whitebox.ai.service;

import com.ssafy.whitebox.ai.entity.AIResult;
import com.ssafy.whitebox.ai.repository.AIResultRepository;
import com.ssafy.whitebox.common.service.FileStorageService;
import com.ssafy.whitebox.user.entity.User;
import com.ssafy.whitebox.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.client.WebClient;
import com.ssafy.whitebox.ai.dto.AIAnalysisResult;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.client.MultipartBodyBuilder;
import reactor.core.publisher.Mono;
import org.springframework.core.io.InputStreamResource;



import java.io.IOException;
import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class AIResultService {

    private final AIResultRepository aiResultRepository;
    private final UserRepository userRepository;
    private final FileStorageService fileStorageService;
    private final WebClient webClient; // WebClient 인스턴스 주입

    // FastAPI 서버 URL
    @Value("${fastapi.server.url}")
    private String fastApiUrl;

    public AIResult createAIResult(Long userId, MultipartFile videoFile) throws IOException {
        User user = userRepository.findById(userId).orElseThrow(() -> new IllegalArgumentException("User not found"));

        // 비디오 파일 저장
        String videoUrl = fileStorageService.saveFile(videoFile, "video");

        // FastAPI로 비디오 파일 전송 및 AI 분석 결과 받기
        AIAnalysisResult analysisResult = analyzeVideo(videoFile);

        // AI 결과 생성 및 저장
        AIResult aiResult = AIResult.builder()
                .user(user)
                .createdAt(LocalDateTime.now())
                .aiRelatedInformation(analysisResult.getAiRelatedInformation())
                .aiRelatedLaw(analysisResult.getAiRelatedLaw())
                .aiUserFault(analysisResult.getAiUserFault())
                .aiOtherFault(analysisResult.getAiOtherFault())
                .videoUrl(videoUrl)
                .thumbnail1("thumbnail1.jpg")
                .thumbnail2("thumbnail2.jpg")
                .thumbnail3("thumbnail3.jpg")
                .isUploaded(false)
                .build();

        return aiResultRepository.save(aiResult);
    }
    private AIAnalysisResult analyzeVideo(MultipartFile videoFile) throws IOException {
        WebClient client = WebClient.builder()
                .baseUrl(fastApiUrl)
                .build();

        MultipartBodyBuilder builder = new MultipartBodyBuilder();
        builder.part("file", videoFile.getResource())
                .filename(videoFile.getOriginalFilename());
        byte[] videoBytes = videoFile.getBytes();
        return client.post()
                .uri("/analyze-video/")
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .body(BodyInserters.fromMultipartData(builder.build()))
                .retrieve()
                .onStatus(status -> status.is4xxClientError() || status.is5xxServerError(),
                        clientResponse -> clientResponse.bodyToMono(String.class)
                                .flatMap(errorBody -> Mono.error(new RuntimeException("FastAPI 오류: " + errorBody))))
                .bodyToMono(AIAnalysisResult.class)
                .block();
    }
    public List<AIResult> getAllAIResults() {
        return aiResultRepository.findAll();
    }

    public AIResult getAIResultById(Long id) {
        return aiResultRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("AI Result not found"));
    }
}
