package com.ssafy.whitebox.community.controller;


import com.ssafy.whitebox.community.entity.Community;
import com.ssafy.whitebox.community.service.CommunityService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import com.ssafy.whitebox.community.dto.CommunityParam;
import com.ssafy.whitebox.community.dto.CommunityUpdateParam;
import org.springframework.data.domain.Page;
import com.ssafy.whitebox.community.dto.PageResponse;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.List;

@RestController
@RequestMapping("/api/v1/community")
@RequiredArgsConstructor
public class CommunityController {

    private final CommunityService communityService;

    @GetMapping
    public ResponseEntity<List<Community>> getAllCommunities() {
        return ResponseEntity.ok(communityService.findAll());
    }

    @GetMapping("/page/{pageIndex}")
    public ResponseEntity<PageResponse<CommunityParam>> getCommunityListWithPagination(
            @PathVariable int pageIndex) {
        int pageSize = 10;  // 한 페이지에 표시할 게시글 수
        Page<CommunityParam> communityPage = communityService.getCommunitiesWithPagination(pageIndex, pageSize);
        long totalCommunities = communityService.getTotalCommunityCount();
        PageResponse<CommunityParam> response = new PageResponse<>(totalCommunities, communityPage.getContent());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{communityId}")
    public ResponseEntity<CommunityParam> getCommunityById(@PathVariable long communityId) {
        CommunityParam communityDTO = communityService.findById(communityId);
        return ResponseEntity.ok(communityDTO);
    }

    @PostMapping
    public ResponseEntity<Community> createCommunity(
            @RequestPart("title") String title,
            @RequestPart("description") String description,
            @RequestPart(value = "images", required = false) List<MultipartFile> images,
            @AuthenticationPrincipal UserDetails userDetails  // 인증된 유저 정보 가져오기
    ) {
        Community community = new Community();
        community.setComTitle(title);
        community.setComDescription(description);
        String userEmail = userDetails.getUsername();  // 인증된 유저 이메일 사용
        return ResponseEntity.ok(communityService.createCommunity(community, images, userEmail));
    }

    @PatchMapping("/{communityId}")
    public ResponseEntity<Community> updateCommunity(
            @PathVariable int communityId,
            @RequestBody CommunityUpdateParam communityUpdateParam,
            @AuthenticationPrincipal UserDetails userDetails  // 인증된 유저 정보 가져오기
    ) {
        String userEmail = userDetails.getUsername();  // 현재 로그인된 유저의 이메일
        CommunityParam existingCommunity = communityService.findById(communityId);

        // 작성자와 로그인된 유저가 일치하는지 확인
        if (!existingCommunity.getUser().userEmail().equals(userEmail)) {
            return ResponseEntity.status(403).build();  // 권한 없음 (403 Forbidden)
        }

        existingCommunity.setComTitle(communityUpdateParam.getComTitle());
        existingCommunity.setComDescription(communityUpdateParam.getComDescription());
        return ResponseEntity.ok(communityService.save(existingCommunity));
    }

    @DeleteMapping("/{communityId}")
    public ResponseEntity<Void> deleteCommunity(
            @PathVariable int communityId,
            @AuthenticationPrincipal UserDetails userDetails  // 인증된 유저 정보 가져오기
    ) {
        String userEmail = userDetails.getUsername();  // 현재 로그인된 유저의 이메일
        CommunityParam existingCommunity = communityService.findById(communityId);

        // 작성자와 로그인된 유저가 일치하는지 확인
        if (!existingCommunity.getUser().userEmail().equals(userEmail)) {
            return ResponseEntity.status(403).build();  // 권한 없음 (403 Forbidden)
        }

        communityService.deleteById(communityId);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{communityId}")
    public ResponseEntity<Void> addComment(
            @PathVariable Long communityId,
            @RequestPart("comment") String comment,
            @AuthenticationPrincipal UserDetails userDetails  // 인증된 유저 정보 가져오기
    ) {
        communityService.addComment(communityId, userDetails.getUsername(), comment);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{communityId}/{commentId}")
    public ResponseEntity<Void> deleteComment(
            @PathVariable Long commentId,
            @AuthenticationPrincipal UserDetails userDetails  // 인증된 유저 정보 가져오기
    ) {
        // 댓글 작성자 확인 및 삭제 권한 확인
        boolean isAuthorized = communityService.isCommentAuthor(commentId, userDetails.getUsername());
        if (!isAuthorized) {
            return ResponseEntity.status(403).build();  // 권한 없음 (403 Forbidden)
        }

        communityService.deleteComment(commentId);
        return ResponseEntity.noContent().build();
    }

}
