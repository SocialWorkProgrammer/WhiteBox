package com.ssafy.whitebox.ai.service;

import com.ssafy.whitebox.ai.entity.Lawyer;
import com.ssafy.whitebox.ai.repository.LawyerRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.Date;

@Service
public class LawyerService {

    private final LawyerRepository lawyerRepository;
    private final WebClient webClient;

    public LawyerService(LawyerRepository lawyerRepository) {
        this.lawyerRepository = lawyerRepository;
        this.webClient = WebClient.builder().baseUrl("http://localhost:8000").build(); // Python 서버의 base URL 설정
    }

    public Lawyer findLawyerByNameAndDate(String name, Date date) {
        return lawyerRepository.findByLawyerNameAndLawyerDate(name, date);
    }

    public ResponseEntity<String> verifyLawyerImageWithPython(String name, Date date, String email, MultipartFile file, String lawyerImageUrl) {
        try {
            // Python 서버에 이미지 검증 요청 전송
            MultiValueMap<String, Object> body = fromMultipartData(name, date, email, file, lawyerImageUrl);

            ResponseEntity<String> response = webClient.post()
                    .uri("/api/v1/lawyer")
                    .bodyValue(body)
                    .retrieve()
                    .toEntity(String.class)
                    .block();

            return response;

        } catch (WebClientResponseException e) {
            e.printStackTrace();
            return ResponseEntity.status(e.getStatusCode()).body("이미지 검증 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    private MultiValueMap<String, Object> fromMultipartData(String name, Date date, String email, MultipartFile file, String lawyerImageUrl) {
        LinkedMultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", file.getResource()); // 업로드된 이미지 파일
        body.add("name", name);
        body.add("date", date);
        body.add("user_email", email);
        body.add("lawyer_image_url", lawyerImageUrl); // 데이터베이스에 있는 변호사 이미지 URL 추가
        return body;
    }
}
