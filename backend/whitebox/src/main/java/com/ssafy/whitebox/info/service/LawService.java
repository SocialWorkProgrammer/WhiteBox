package com.ssafy.whitebox.info.service;
import com.ssafy.whitebox.info.entity.Law;
import com.ssafy.whitebox.info.repository.LawRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor
public class LawService {
    private final LawRepository lawRepository;

    public List<Law> getLawsByPage(int page) {
        return lawRepository.findByPageOrderByLawNumberAscSeqAsc(page);
    }
}
