package com.ssafy.whitebox.common.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

@Service
public class FileStorageService {

    private static final String IMAGE_UPLOAD_DIR = "backend/whitebox/src/main/resources/static/images";
    private static final String VIDEO_UPLOAD_DIR = "backend/whitebox/src/main/resources/static/videos"; // 동영상 저장 경로 추가

    // 파일 저장 메서드
    public String saveFile(MultipartFile file, String type) throws IOException {
        String uploadDir = type.equals("image") ? IMAGE_UPLOAD_DIR : VIDEO_UPLOAD_DIR;

        // 파일명을 UUID로 변경하여 저장 (중복 방지)
        String originalFilename = file.getOriginalFilename();
        String fileExtension = getFileExtension(originalFilename);
        String savedFileName = UUID.randomUUID().toString() + fileExtension;
        Path savePath = Paths.get(uploadDir, savedFileName);

        // 디렉터리가 존재하지 않으면 생성
        if (!Files.exists(savePath.getParent())) {
            Files.createDirectories(savePath.getParent());
        }

        // 파일 저장
        Files.write(savePath, file.getBytes());

        return savedFileName; // 저장된 파일명 반환
    }

    // 파일 확장자를 가져오는 메서드
    private String getFileExtension(String fileName) {
        if (fileName != null && fileName.contains(".")) {
            return fileName.substring(fileName.lastIndexOf("."));
        }
        return "";
    }
}
