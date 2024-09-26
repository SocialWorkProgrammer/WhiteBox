package com.ssafy.whitebox.info.service;
import com.ssafy.whitebox.info.entity.Law;
import com.ssafy.whitebox.info.repository.LawRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class LawService {
    private final LawRepository lawRepository;

    public List<Law> getLawsByPage(int page) {
        return lawRepository.findByPageOrderByLawNumberAscSeqAsc(page);
    }

    public Map<String, Object> processLaws(List<Law> laws) {
        Map<String, Object> response = new HashMap<>();

        // seq == 1 인 법의 날짜 정보를 response에 추가
        laws.stream()
                .filter(law -> law.seq() == 1)
                .findFirst()
                .ifPresent(law -> {
                    response.put("startDate", law.startDate());
                    response.put("announceDate", law.announceDate());
                });

        // 법 번호별로 그룹핑하고, 설명을 리스트로 저장
        Map<Integer, List<String>> groupedByLawNumber = laws.stream()
                .collect(Collectors.groupingBy(Law::lawNumber,
                        Collectors.mapping(Law::lawDescription, Collectors.toList())));

        for (Map.Entry<Integer, List<String>> entry : groupedByLawNumber.entrySet()) {
            Integer lawNumber = entry.getKey();
            List<String> descriptions = entry.getValue();

            response.put(String.valueOf(lawNumber), descriptions);
        }

        return response;
    }
}
