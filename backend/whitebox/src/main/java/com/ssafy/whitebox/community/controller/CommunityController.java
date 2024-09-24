package com.ssafy.whitebox.community.controller;

import com.ssafy.whitebox.community.dto.CommentCreateParam;
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

        // 한 페이지에 표시할 게시글 수 (예: 10개)
        int pageSize = 10;

        // 페이징된 게시글 목록과 총 게시글 수를 가져옴
        Page<CommunityParam> communityPage = communityService.getCommunitiesWithPagination(pageIndex, pageSize);
        long totalCommunities = communityService.getTotalCommunityCount();

        // 응답 객체 생성 (총 게시글 수와 페이징된 게시글 포함)
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
        String userEmail = userDetails.getUsername();  // 또는 토큰에 저장된 userId를 가져오는 방식으로 변경 가능
        return ResponseEntity.ok(communityService.createCommunity(community, images, userEmail));
    }

    @PatchMapping("/{communityId}")
    public ResponseEntity<Community> updateCommunity(@PathVariable int communityId, @RequestBody CommunityUpdateParam community) {
        CommunityParam existingCommunity = communityService.findById(communityId);
        existingCommunity.setComTitle(community.getComTitle());
        existingCommunity.setComDescription(community.getComDescription());
        return ResponseEntity.ok(communityService.save(existingCommunity));
    }

    @DeleteMapping("/{communityId}")
    public ResponseEntity<Void> deleteCommunity(@PathVariable int communityId) {
        communityService.deleteById(communityId);
        return ResponseEntity.noContent().build();
    }
    // 댓글 작성 API
    @PostMapping("/{communityId}")
    public ResponseEntity<Void> addComment(@PathVariable Long communityId,
                                           @RequestPart("comment") String comment,
                                           @AuthenticationPrincipal UserDetails userDetails  // 인증된 유저 정보 가져오기
                                           ) {

        communityService.addComment(communityId, userDetails.getUsername(), comment);  // comment로 수정
        return ResponseEntity.ok().build();
    }

    // 댓글 삭제 API
    @DeleteMapping("/{communityId}/{commentId}")
    public ResponseEntity<Void> deleteComment(@PathVariable Long commentId) {
        communityService.deleteComment(commentId);
        return ResponseEntity.noContent().build();
    }

}
