package com.ssafy.whitebox.info.controller;

import com.ssafy.whitebox.info.entity.RelatedSites;
import com.ssafy.whitebox.info.service.RelatedSitesService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@Tag(name="RelatedSites", description = "법률 정보 관련 사이트 API 명세")
@RestController
@RequestMapping("api/v1/board")
@RequiredArgsConstructor
public class RelatedSitesController {

    private final RelatedSitesService relatedSitesService;
    @Operation(summary = "법률 정보 사이트 제공 API")
    @ApiResponse(
            responseCode = "200",
            description = "법률 정보 사이트 제공 완료"
    )
    @GetMapping("/related-sites")
    public ResponseEntity<List<RelatedSites>> getAllRelatedSites() {
        List<RelatedSites> relatedSites = relatedSitesService.getAllRelatedSites();
        return new ResponseEntity<>(relatedSites, HttpStatus.OK);

    }
}
