package com.ssafy.whitebox.ai.dto;

import lombok.Data;

@Data
public class AIAnalysisResult {
    private String aiRelatedInformation;
    private String aiRelatedLaw;
    private int aiUserFault;
    private int aiOtherFault;
}
