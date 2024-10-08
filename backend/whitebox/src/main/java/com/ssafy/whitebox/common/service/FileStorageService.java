package com.ssafy.whitebox.common.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

@Service
public class FileStorageService {

    @Value("${file.upload-dir.images}")
    private String imageUploadDir;

    @Value("${file.upload-dir.videos}")
    private String videoUploadDir;

    @Value("${file.upload-dir.thumbnails}")
    private String thumbnailUploadDir; // 썸네일 이미지 경로

    // 파일 저장 메서드
    public String saveFile(MultipartFile file, String type) throws IOException {
        return saveFile(file.getBytes(), file.getOriginalFilename(), type);
    }

    // File 타입의 파일 저장 메서드
    public String saveFile(File file, String type) throws IOException {
        return saveFile(Files.readAllBytes(file.toPath()), file.getName(), type);
    }

    // 실제 파일 저장을 수행하는 메서드
    private String saveFile(byte[] fileBytes, String originalFilename, String type) throws IOException {
        String uploadDir;
        switch (type) {
            case "image":
                uploadDir = imageUploadDir;
                break;
            case "video":
                uploadDir = videoUploadDir;
                break;
            case "thumbnail":
                uploadDir = thumbnailUploadDir;
                break;
            default:
                throw new IllegalArgumentException("Invalid file type: " + type);
        }

        // 파일명을 UUID로 변경하여 저장 (중복 방지)
        String fileExtension = getFileExtension(originalFilename);
        String savedFileName = UUID.randomUUID().toString() + fileExtension;
        Path savePath = Paths.get(uploadDir, savedFileName);

        // 디렉터리가 존재하지 않으면 생성
        if (!Files.exists(savePath.getParent())) {
            Files.createDirectories(savePath.getParent());
        }

        // 파일 저장
        Files.write(savePath, fileBytes);
        System.out.println("File saved at: " + savePath.toString());
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
