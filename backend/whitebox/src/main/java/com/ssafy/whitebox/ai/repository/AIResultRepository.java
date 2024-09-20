package com.ssafy.whitebox.ai.repository;

import com.ssafy.whitebox.ai.entity.AIResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AIResultRepository extends JpaRepository<AIResult, Long> {
    // 추가 쿼리 메서드 정의 가능
}