package com.ssafy.whitebox.info.dto;


import com.ssafy.whitebox.info.entity.Law;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
@Schema(description = "바뀐 법 정보")
public class LawParam {
    @Schema(description = "페이지 정보")
    int page;

    @Schema(description = "법 시행 날짜")
    String startDate;

    @Schema(description = "법 공포 날짜")
    String announceDate;

    @Schema(description = "법 조문 번호 ")
    int lawNumber;

    @Schema(description = "법 조문 내용")
    String lawDescription;


    public static LawParam from(Law law){
        LawParam lawParam = new LawParam();
        lawParam.page = law.page();
        lawParam.startDate = law.startDate();
        lawParam.announceDate = law.announceDate();
        lawParam.lawNumber = law.lawNumber();
        lawParam.lawDescription = law.lawDescription();
        return lawParam;
    }
}
