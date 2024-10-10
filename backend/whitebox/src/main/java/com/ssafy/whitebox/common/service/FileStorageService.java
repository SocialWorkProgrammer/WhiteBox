package com.ssafy.whitebox.common.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.UUID;

@Service
public class FileStorageService {

    private final S3Service s3Service;

    public FileStorageService(S3Service s3Service) {
        this.s3Service = s3Service;
    }

    // MultipartFile 저장 메서드
    public String saveFile(MultipartFile file, String type) throws IOException {
        return saveFile(file.getBytes(), file.getOriginalFilename(), type);
    }

    // File 타입의 파일 저장 메서드
    public String saveFile(File file, String type) throws IOException {
        return saveFile(Files.readAllBytes(file.toPath()), file.getName(), type);
    }

    // 실제 파일 저장을 수행하는 메서드
    private String saveFile(byte[] fileBytes, String originalFilename, String type) throws IOException {
        // 파일명을 UUID로 변경하여 저장 (중복 방지)
        String fileExtension = getFileExtension(originalFilename);
        String savedFileName = UUID.randomUUID().toString() + fileExtension;
        String key = getS3UploadDirectory(type) + "/" + savedFileName;

        // S3에 파일 업로드
        return s3Service.uploadFile(fileBytes, key);
    }

    // 파일 타입에 따른 S3 경로 설정 메서드
    private String getS3UploadDirectory(String type) {
        switch (type) {
            case "image":
                return "images";
            case "video":
                return "videos";
            case "thumbnail":
                return "thumbnails";
            case "video/mp4":
                return "video/mp4";
            default:
                throw new IllegalArgumentException("Invalid file type: " + type);
        }
    }

    // 파일 확장자를 가져오는 메서드
    private String getFileExtension(String fileName) {
        if (fileName != null && fileName.contains(".")) {
            return fileName.substring(fileName.lastIndexOf("."));
        }
        return "";
    }
}
